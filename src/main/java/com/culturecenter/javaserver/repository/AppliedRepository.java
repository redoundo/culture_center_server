package com.culturecenter.javaserver.repository;

import com.culturecenter.javaserver.dto.LecturesInterface;
import com.culturecenter.javaserver.entity.Applied;
import com.culturecenter.javaserver.entity.Lectures;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Repository
public interface AppliedRepository extends JpaRepository<Applied, Integer> {

    /**
     * 사용자 아이디를 가진 지원한 강좌 내역 삭제
     * @param lectureId 강좌 아이디
     * @param userId 사용자 아이디
     */
    @Modifying
    @Query(value = "DELETE FROM Applied applied WHERE applied.appliedLectureId=:lectureId AND applied.appliedUserId=:userId")
    void deleteAppliedByUserId(@Param("lectureId") Integer lectureId, @Param("userId") Integer userId);

    /**
     * 사용자 아이디를 가지고 있는 모든 지원한 강좌 내용을 삭제
     * @param userId 사용자 아이디
     */
    @Modifying
    @Query(value = "DELETE FROM Applied applied WHERE applied.appliedUserId=:userId")
    void deleteAllAppliedByUserId(@Param("userId") Integer userId);

    @Query(value = "SELECT lectures.lectureId  AS lectureId, lectures.center AS center, lectures.type AS type, lectures.region AS region, "
            + "lectures.branch  AS branch, lectures.address AS address, lectures.target AS target,lectures.category AS category,lectures.title AS title,lectures.url AS url,"
            + "lectures.src AS src,lectures.content AS content,lectures.adult AS adult, lectures.price AS price,"
            + "lectures.kid AS kid, lectures.baby AS baby, lectures.lectureStart AS lectureStart, lectures.lectureEnd AS lectureEnd,"
            + " lectures.enrollStart AS enrollStart, lectures.enrollEnd AS enrollEnd, lectures.lectureSupplies AS lectureSupplies,"
            + " lectures.curriculum AS curriculum, lectures.crawledDate AS crawledDate, lectures.lectureHeldDates AS lectureHeldDates"
            + " FROM Applied applied INNER JOIN Lectures lectures ON applied.appliedUserId=:userId AND lectures.lectureId=applied.appliedLectureId")
    List<LecturesInterface> allLectureByUserId(@Param("userId") Integer userId);
}
