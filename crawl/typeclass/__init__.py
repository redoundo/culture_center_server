from . import CenterInfoNoLink, CenterInfoWithLink, ClassIdInfoType, LectureType
import sys
sys.path.append("..")

__all__ = ["CenterInfoNoLink", "CenterInfoWithLink", "ClassIdInfoType", "LectureType"]
ClassIdInfo = ClassIdInfoType
NoLink = CenterInfoNoLink
WithLink = CenterInfoWithLink
Lecture = LectureType
