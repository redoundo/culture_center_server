package com.culturecenter.javaserver.utils;

import com.culturecenter.javaserver.dto.SearchConditions;

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
        if (!whereCause.isEmpty()) sql = sql + " WHERE " + String.join(" AND ", whereCause) + ";";
        else sql = sql + ";";
        return sql;
    }
}
