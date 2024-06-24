package com.culturecenter.javaserver.dto;


import java.sql.Timestamp;
import java.util.Map;

/**
 * join 된 테이블에서 lectures 테이블의 내용만을 가져오기 위한 인터페이스
 */
public interface LecturesInterface {
    Integer getLectureId();
    String getCenter();
    String getType();
    String getRegion();
    String getBranch();
    String getAddress();
    String getCategory();
    String getTarget();
    Integer getPrice();
    String getTitle();
    String getSrc();
    String getUrl();
    String getContent();
    String getAdult();
    String getKid();
    String getBaby();
    Timestamp getLectureStart();
    Timestamp getLectureEnd();
    Timestamp getEnrollStart();
    Timestamp getEnrollEnd();
    Timestamp getCrawledDate();
    Map<String, Object> getCurriculum();
    String getLectureSupplies();
    String getLectureHeldDates();
    String getEnrollStatus();

}
