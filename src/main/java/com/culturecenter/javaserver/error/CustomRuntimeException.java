package com.culturecenter.javaserver.error;

import lombok.Getter;

/**
 * error code 를 담는 클래스
 */
@Getter
public class CustomRuntimeException extends RuntimeException{
    ErrorCode errorCode;
    public CustomRuntimeException(ErrorCode error){
        this.errorCode = error;
    }
}
