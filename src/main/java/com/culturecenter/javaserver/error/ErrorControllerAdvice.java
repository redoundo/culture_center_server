package com.culturecenter.javaserver.error;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import static com.culturecenter.javaserver.error.ErrorResponses.setErrorResponse;

/**
 * 전역 예외 처리자
 */
@RestControllerAdvice
public class ErrorControllerAdvice {
    /**
     * 에러 처리자. 성공의 경우 별도의 내용이 필요하기 때문에 제공하지 않음.
     * @param err 에러 내용.
     * @return 에러 내용이 담긴 responseEntity.
     */
    @ExceptionHandler(CustomRuntimeException.class)
    public ResponseEntity<ErrorResponses> handlingError(CustomRuntimeException err){
        return setErrorResponse(err.errorCode);
    }
}
