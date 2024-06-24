package com.culturecenter.javaserver.repository;

import com.culturecenter.javaserver.entity.Centers;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CenterRepository extends JpaRepository<Centers, Integer> {

    @Query(value = "SELECT center FROM Centers center WHERE center.centerType=:type")
    List<Centers> selectCentersByType (@Param("type") String type);
}
