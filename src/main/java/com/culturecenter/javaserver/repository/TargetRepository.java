package com.culturecenter.javaserver.repository;

import com.culturecenter.javaserver.entity.Targets;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TargetRepository extends JpaRepository<Targets, Integer> {
}
