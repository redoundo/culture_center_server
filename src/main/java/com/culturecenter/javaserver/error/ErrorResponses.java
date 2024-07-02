package com.culturecenter.javaserver.error;

import lombok.Builder;
import lombok.Data;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/**
 * 에러일 경우 해당 에러 내용을 반환하는 responseEntity 생성.
 */
@Data
@Builder
public class ErrorResponses {
    private String errorName;
    private HttpStatus status;
    private String statusMessage;

    /**
     * 에러 내용을 담은 responseEntity 반환.
     * @param err 문제 내용.
     * @return 문제 내용이 담긴 responseEntity
     */
    public static ResponseEntity<ErrorResponses> setErrorResponse(ErrorCode err){
        return ResponseEntity
                .status(err.getStatus())
                .body(ErrorResponses.builder()
                        .errorName(err.name())
                        .statusMessage(err.getStatusMessage())
                        .status(err.getStatus())
                        .build());

    }
}
