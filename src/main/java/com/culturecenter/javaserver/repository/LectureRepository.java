package com.culturecenter.javaserver.repository;

import com.culturecenter.javaserver.entity.Lectures;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.scheduling.annotation.Async;

import java.util.concurrent.CompletableFuture;

public interface LectureRepository extends JpaRepository<Lectures, Integer>, JpaSpecificationExecutor<Lectures>{

    @Modifying
    @Query("UPDATE Lectures lecture SET lecture.enrollStatus=:status WHERE lecture.lectureId=:lectureId")
    void updateEnrollStatus(@Param("lectureId")Integer lectureId, @Param("status") String status);

    @Async
    CompletableFuture<Lectures> findByLectureId(Integer lectureId);
}
