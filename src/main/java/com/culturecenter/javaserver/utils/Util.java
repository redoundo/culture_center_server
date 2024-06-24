package com.culturecenter.javaserver.utils;

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
}
