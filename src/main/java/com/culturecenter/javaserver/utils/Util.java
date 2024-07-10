package com.culturecenter.javaserver.utils;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.dto.SearchResultsDto;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

/**
 * 유틸리티 클래스
 */
public class Util {
    public static Util checking = new Util();

    /**
     * 문자열 유효성 확인
     * @param needCheck 확인할 문자열
     * @return 유효성 여부
     */
    public boolean checkString(String needCheck){
        return needCheck != null && !needCheck.isEmpty() && !needCheck.equals("null");
    }

    /**
     * 최대/ 최소 경도, 위도 계산
     * @param latitude 위도
     * @param longitude 경도
     * @param distance 이동할 거리
     * @return [min latitude, max latitude, min longitude, max longitude] == [남, 북, 서, 동]
     */
    public double[] calculateLocation (double latitude, double longitude, double distance) {
        // 위도와 경도를 라디안으로 변환
        double radLat = Math.toRadians(latitude);
        double radLon = Math.toRadians(longitude);
        // 이동할 거리 또한 라디안으로 변환
        double radDist = distance / 6371e3;
        // 최대/ 최소 위도 계산
        double minLat = radLat - radDist;
        double maxLat = radLat + radDist;
        // 위도에 따라 경도의 변화량이 달라지므로, 이를 반영해 최대/최소 경도 계산
        double minLon = radLon - radDist / Math.cos(radLat);
        double maxLon = radLon + radDist / Math.cos(radLat);

        return new double[]{
                Math.toDegrees(minLat),
                Math.toDegrees(maxLat),
                Math.toDegrees(minLon),
                Math.toDegrees(maxLon)
        };
    }

    public String createSqlStatementByConditions(SearchConditions conditions){
        String sql = "SELECT * FROM lectures ";
        List<String> whereCause = new ArrayList<>();
        if (checking.checkString(conditions.getTarget()) && !checking.checkString(conditions.getCategory()))
            whereCause.add("%s IS NOT NULL".formatted(conditions.getTarget()));
        if (checking.checkString(conditions.getCategory()) && checking.checkString(conditions.getTarget()))
            whereCause.add("%s IS NOT NULL AND %s='%s'".formatted(conditions.getTarget(), conditions.getTarget(), conditions.getCategory()));
        if (checking.checkString(conditions.getKeyword()))
            whereCause.add("title LIKE '%s'".formatted(conditions.getKeyword()));
        if (checking.checkString(conditions.getCenterType()))
            whereCause.add("type='%s'".formatted(conditions.getCenterType()));
        if (checking.checkString(conditions.getCenterName()))
            whereCause.add("center='%s'".formatted(conditions.getCenterName()));
        if (checking.checkString(conditions.getAddress()))
            whereCause.add("address='%s'".formatted(conditions.getAddress()));
        if (conditions.getLatitude() != null && conditions.getLongitude() != null){
            double[] lonAndLat = calculateLocation(conditions.getLatitude(), conditions.getLongitude(), 300);
            whereCause.add("branch IN (SELECT branchName FROM branches WHERE branches.longitude BETWEEN %s AND %s AND branches.latitude BETWEEN %s AND %s)".formatted(lonAndLat[2], lonAndLat[3], lonAndLat[0], lonAndLat[1]));
        }
        if (!whereCause.isEmpty()) sql = sql + " WHERE " + String.join(" AND ", whereCause);
        if(conditions.getPage() != null) sql = sql + " LIMIT 0,%s".formatted((conditions.getPage() * 16)) + ";";
        else sql = sql + " LIMIT 0,16;";
        return sql;
    }

    public String javaObjectToJson(SearchResultsDto results){
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.writeValueAsString(results);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public <T> String javaObjectToJson (T values){
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.writeValueAsString(values);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public <T> T jsonToJavaObject(String cached, Class<T> clazz){
        if(!checkString(cached)) return null;
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            JavaType javaType = objectMapper.getTypeFactory().constructType(clazz);
            return objectMapper.readValue(cached, javaType);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public <T> boolean sameContentObject(T obj1, T obj2) {
        if (obj1 == obj2) return true;
        if (obj1 == null || obj2 == null) return false;
        if (!obj1.getClass().equals(obj2.getClass())) return false;

        Field[] fields = obj1.getClass().getDeclaredFields();
        for (Field field : fields) {
            field.setAccessible(true);
            try {
                Object value1 = field.get(obj1);
                Object value2 = field.get(obj2);
                if (value1 == null && value2 == null) continue;
                if (value1 == null || value2 == null) return false;
                if (!value1.equals(value2)) return false;
            } catch (IllegalAccessException e) {
                e.printStackTrace();
                return false;
            }
        }
        return true;
    }
}
