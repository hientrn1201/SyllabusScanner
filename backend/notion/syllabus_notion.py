from notion.notion_base import Notion


class SyllabusNotion(Notion):
    def __init__(self, notion_api_key, notion_database_id, syllabus_data):
        self.course_title = syllabus_data['course_title']
        self.course_description = syllabus_data['course_description']
        self.locations = syllabus_data.get('location', [])
        self.meet_time = syllabus_data.get('meet_time', [])
        self.professors = syllabus_data.get('professors', [])
        self.office_hour = syllabus_data.get('office_hour', [])
        self.additional_info = syllabus_data.get('additional_info', 'N/A')
        self.cut_offs = syllabus_data.get('grading', {}).get('cut_offs', {})
        self.grading_components = syllabus_data.get(
            'grading', {}).get('components', {})
        super().__init__(notion_api_key, notion_database_id)

    def _create_instructors_column(self, instructors):
        name_column = [self._create_block(
            "paragraph", "Instructors:", {"bold": True})]
        email_column = [self._create_block(
            "paragraph", "Email:", {"bold": True})]

        for instructor in instructors:
            name_column.append(self._create_block(
                "paragraph", instructor["prof_name"]))
            email_column.append(self._create_block(
                "paragraph", instructor["prof_email"]))
        return self._create_columns([name_column, email_column])

    def _create_hours_column(self, lecture_hours, office_hours):
        lecture_column = [self._create_block(
            "paragraph", "Lecture:", {"bold": True})]
        oh_column = [self._create_block(
            "paragraph", "Office Hours:", {"bold": True})]

        if lecture_hours:
            for time in lecture_hours:
                lecture_column.append(self._create_block(
                    "paragraph", f"{time['day']} {time['start_time']}-{time['end_time']}"))
        else:
            lecture_column.append(self._create_block("paragraph", "N/A"))

        if office_hours:
            for time in office_hours:
                oh_column.append(self._create_block(
                    "paragraph", f"{time['day']} {time['start_time']}-{time['end_time']}"))
        else:
            oh_column.append(self._create_block("paragraph", "N/A"))
        return self._create_columns([lecture_column, oh_column])

    def _create_cutoff_table(self, cutoffs):
        letters = []
        cutoff_scores = []
        for data in cutoffs:
            letters.append(data['letter_grade'])
            cutoff_scores.append(str(data['cutoff_score']))
        return self._create_table([letters, cutoff_scores], len(letters))

    def create_syllabus_notion_page(self):
        children = [
            self._create_block("heading_2", "Course Description"),
            self._create_block("paragraph", self.course_description),
            self._create_block("paragraph", "Location", {"bold": True}),
            self._create_block("paragraph", " ".join(
                [location for location in self.locations]) if self.locations else "N/A"),
            self._create_instructors_column(
                self.professors) if self.professors else self._create_block("paragraph", ""),
            self._create_hours_column(self.meet_time, self.office_hour),
            self._create_block("heading_2", "Grading"),
            self._create_block("heading_3", "Cutoffs"),
            self._create_cutoff_table(
                self.cut_offs) if self.cut_offs else self._create_block("paragraph", "N/A"),
            self._create_block("heading_3", "Grading components"),
        ]
        grading_components = [self._create_block("paragraph", f"{component['component_name']}: {component['percentage']}%")
                              for component in self.grading_components] if self.grading_components else [self._create_block("paragraph", "N/A")]
        children.extend(grading_components)
        children.extend([self._create_block("heading_2", "Additional Information"),
                        self._create_block("paragraph", self.additional_info or "")])
        return self._create_notion_page(self.course_title, children)
