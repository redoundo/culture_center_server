package com.culturecenter.javaserver.repository;

import com.culturecenter.javaserver.entity.Lectures;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface LectureRepository extends JpaRepository<Lectures, Integer>, JpaSpecificationExecutor<Lectures>{

    @Query("UPDATE Lectures lecture SET lecture.enrollStatus=:status WHERE lecture.lectureId=:lectureId")
    void updateEnrollStatus(@Param("lectureId")Integer lectureId, @Param("status") String status);
}
