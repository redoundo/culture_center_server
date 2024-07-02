package com.culturecenter.javaserver.dto;

import jakarta.annotation.Nullable;
import lombok.*;

import java.util.List;

@Builder
@Getter
@Setter
@AllArgsConstructor
@RequiredArgsConstructor
public class AddressFromGeoApiDto {
    private Status status;
    private List<GeoAddressResult> results;

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Status{
         Integer code;
         String name;
         String message;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class GeoAddressResult {
        String name;
        Code code;
        Region region;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Code {
        String id;
        String type;
        String mappingId;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Region {
        Area area0;
        Area area1;
        Area area2;
        Area area3;
        Area area4;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Area {
        String name;
        Coords coords;
        @Nullable String alias;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Coords {
        Center center;
    }

    @Getter
    @Setter
    @AllArgsConstructor
    @RequiredArgsConstructor
    static class Center {
        String crs;
        Double x;
        Double y;
    }

}
