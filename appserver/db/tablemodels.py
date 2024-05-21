from datetime import datetime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, JSON, DateTime


class Base(DeclarativeBase):
    pass


class Lectures(Base):
    __tablename__ = 'lectures'
    lectureId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, nullable=False)
    center: Mapped[str] = mapped_column(String(90), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    region: Mapped[str] = mapped_column(String(60), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    target: Mapped[str] = mapped_column(String(90), nullable=False)
    category: Mapped[str] = mapped_column(String(90), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    src: Mapped[str] = mapped_column(String(300), nullable=False)
    content: Mapped[str] = mapped_column(String(3000), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    adult: Mapped[str] = mapped_column(String(100))
    kid: Mapped[str] = mapped_column(String(100))
    baby: Mapped[str] = mapped_column(String(100))
    lectureStart: Mapped[datetime] = mapped_column(nullable=False, type_=DateTime)
    lectureEnd: Mapped[datetime] = mapped_column(nullable=False, type_=DateTime)
    enrollStart: Mapped[datetime] = mapped_column(nullable=True, type_=DateTime)
    enrollEnd: Mapped[datetime] = mapped_column(nullable=True, type_=DateTime)
    lectureSupplies: Mapped[str] = mapped_column(String(200), nullable=True)
    curriculum: Mapped[Optional[dict]] = mapped_column(nullable=True, type_=JSON)
    crawledDate: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=False, type_=DateTime)
    lectureHeldDates: Mapped[str] = mapped_column(String(500), nullable=False)

    def dictionary(self) -> dict:
        return {
            "lectureId": self.lectureId, "center": self.center, "type": self.type, "region": self.region, "branch": self.branch,
            "address": self.address, "target": self.target, "category": self.category, "title": self.title, "url": self.url,
            "src": self.src, "content": self.content, "price": self.price, "lectureStart": self.lectureStart,
            "lectureEnd": self.lectureEnd, "enrollStart": self.enrollStart, "enrollEnd": self.enrollEnd,
            "lectureSupplies": self.lectureSupplies, "curriculum": self.curriculum, "crawledDate": self.crawledDate,
            "lectureHeldDates": self.lectureHeldDates
        }


class Centers(Base):
    __tablename__ = "centers"
    centerId: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)
    centerName: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    centerType: Mapped[str] = mapped_column(String(45), nullable=False)
    centerUrl: Mapped[str] = mapped_column(String(200), nullable=False)

    def dictionary(self):
        return {"centerId": self.centerId, "centerName": self.centerName, "centerType": self.centerType, "centerUrl": self.centerUrl}


class Categories(Base):
    __tablename__ = "categories"
    categoryId: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    categoryName: Mapped[str] = mapped_column(String(100), nullable=False)
    targetId: Mapped[int] = mapped_column(nullable=False)

    def dictionary(self):
        return {"categoryId" : self.categoryId, "categoryName": self.categoryName, "targetId": self.targetId}

class Targets(Base):
    __tablename__ = "targets"
    targetId: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    targetName: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)

    def dictionary(self):
        return {"targetId": self.targetId, "targetName": self.targetName}

class Branches(Base):
    __tablename__ = "branches"
    branchId: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    branchName: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    branchAddress: Mapped[str] = mapped_column(String(255), nullable=False)
    centerIdOfBranch: Mapped[int] = mapped_column(nullable=False)

    def dictionary(self):
        return {
            "branchId": self.branchId, "branchName": self.branchName, "branchAddress": self.branchAddress, "centerIdOfBranch": self.centerIdOfBranch
        }


class Applied(Base):
    __tablename__ = "applied"
    appliedId: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    appliedLectureId: Mapped[int] = mapped_column(nullable=False)
    appliedUserId: Mapped[int] = mapped_column(nullable=False)

    def dictionary(self):
        return {
            "appliedId": self.appliedId, "appliedLectureId": self.appliedLectureId, "appliedUserId": self.appliedUserId
        }


class Liked(Base):
    __tablename__ = "liked"
    likedId: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    likedLectureId: Mapped[int] = mapped_column(nullable=False)
    likedUserId: Mapped[int] = mapped_column(nullable=False)

    def dictionary(self):
        return {
            "liekdId": self.likedId, "likedLectureId": self.likedLectureId, "likedUserId": self.likedUserId
        }


class Users(Base):
    __tablename__ = "users"
    userId: Mapped[int] = mapped_column(unique=True, autoincrement=True, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    registerDate: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(), onupdate=False,
                                                   type_=DateTime)
    snsProvider: Mapped[str] = mapped_column(String(255), nullable=False)
    snsProviderId: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    wantFcmMessage: Mapped[bool] = mapped_column()
    fcmToken: Mapped[str] = mapped_column(String(500), unique=True)

    def dictionary(self) -> dict:
        return {
            "userId": self.userId, "email": self.email, "nickname": self.nickname, "password": self.password,
            "registerDate": self.registerDate, "snsProvider": self.snsProvider, "snsProviderId": self.snsProviderId,
            "wantFcmMessage": self.wantFcmMessage, "fcmToken": self.fcmToken
        }

