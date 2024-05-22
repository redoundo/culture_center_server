from . import CenterInfoNoLink, CenterInfoWithLink, ClassIdInfoType, LectureType
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("..")
sys.path.append("")

__all__ = ["CenterInfoNoLink", "CenterInfoWithLink", "ClassIdInfoType", "LectureType"]
ClassIdInfo = ClassIdInfoType
NoLink = CenterInfoNoLink
WithLink = CenterInfoWithLink
Lecture = LectureType
