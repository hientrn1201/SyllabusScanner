from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class DayEnum(str, Enum):
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'


class Time(BaseModel):
    day: DayEnum = Field(description="Days when the class meets")
    time: str = Field(description="Time of day when the class meets")


class Instructor(BaseModel):
    prof_name: str = Field(description="Professor/ Instructor Name")
    prof_email: str = Field(description="Professor/ Instructor Email")


class Component(BaseModel):
    component_name: str = Field(
        description="Grading component name (e.g Homework)")
    percentage: float = Field(description='The percentage of the component')


class Cutoff(BaseModel):
    letter_grade: str = Field(description="Letter grade (e.g A, A-, B+, etc)")
    cutoff_score: str = Field(
        description="The score/percentage that required to achieve the correspond letter grade")


class Grading(BaseModel):
    cut_offs: Optional[List[Cutoff]] = Field(
        description="Letter grade and its cutoff score (e.g 'A': 93, etc)")
    components: Optional[List[Component]] = Field(
        description="Different components and their corresponding grading percentage")


class Course(BaseModel):
    course_title: str = Field(description="Course title")
    course_description: str = Field(
        description="General discription of the class")
    location: Optional[List[str]] = Field(
        description="The location of the class (which classroom)")
    meet_time: Optional[List[Time]] = Field(
        description="List of day and time when the class meets")
    professors: List[Instructor] = Field(
        description="List of professors teaching the class")
    office_hour: Optional[List[Time]] = Field(
        description="List of day and time when the professor holds offce hours")
    grading: Optional[Grading] = Field(description="Grading information")
    additional_info: Optional[str] = Field(
        description="Any relevant important information in the syllabus")
