package com.culturecenter.javaserver.error;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * 애러 코드
 */
@Getter
public enum ErrorCode {
    JWT_IS_VALID_BUT_SOMETHING_GOT_WRONG(HttpStatus.INTERNAL_SERVER_ERROR, "jwt 토큰은 유효하나, 내부에서 무언가가 잘못되었습니다."),
    SELECT_FAILED_ERROR(HttpStatus.INTERNAL_SERVER_ERROR ,   "게시물들을 가져오는데 실패했습니다") ,
    DELETE_FAILED_ERROR(HttpStatus.INTERNAL_SERVER_ERROR ,   "게시물을 삭제하는데 실패했습니다") ,
    UPDATE_FAILED_ERROR(HttpStatus.INTERNAL_SERVER_ERROR ,  "게시물을 수정하는데 실패했습니다") ,
    INSERT_FAILED_ERROR(HttpStatus.INTERNAL_SERVER_ERROR ,  "게시물을 생성하는데 실패했습니다") ,
    NO_SUCH_DATA_ERROR (HttpStatus.NOT_FOUND, "해당 내용이 존재하지 않습니다."),
    STATUS_UPDATE_ELEMENT_NOT_EXIST(HttpStatus.INTERNAL_SERVER_ERROR, "강좌 페이지에서 상태 정보를 가져올 수 없습니다."),
    /**
     * update , insert 에 반드시 필요한 내용 중 일부가 존재하지 않을 때.
     */
    MISSING_CONTENT_ERROR(HttpStatus.BAD_REQUEST ,   "필요한 내용이 충족되지 않았습니다") ,
    /**
     * 데이터베이스의 비밀번호와 사용자가 입력한 비밀번호가 동일하지 않을 때.
     */
    MISMATCH_PASSWORD_ERROR(HttpStatus.FORBIDDEN ,  "비밀번호가 일치하지 않습니다") ,
    /**
     * 존재하지 않는 파일을 다운로드 하려고 할때.
     */
    CANT_FIND_FILE_ERROR(HttpStatus.NOT_FOUND ,  "해당 파일이 존재하지 않습니다"),
    /**
     * resource.contentLength() 에서 resource 를 닫지 못해 생기는 예외이다. 대처 방안이 없으므로 일단 예외로 등록한다.
     */
    IOEXCEPTION_WHILE_DOWNLOAD_FILE(HttpStatus.INTERNAL_SERVER_ERROR ,  "파일을 다운로드 하는 중에 문제가 발생했습니다."),
    /**
     * 존재하지 않는 contentId 를 가진 url 로 진입시.
     */
    INVALID_CONTENT_ID_ERROR(HttpStatus.NOT_FOUND  ,  "해당 게시물이 존재하지 않습니다") ,
    /**
     * 문자열의 유효성에 문제가 있을 경우 발생. null , blank , empty
     */
    INVALID_STRING_ARGUMENT(HttpStatus.BAD_REQUEST ,  "문자열이 null 이거나 , 비어있거나 혹은 값이 없습니다"),
    /**
     * 파이 삭제되지 않았을 때 발생하는 에러
     */
    FILE_NOT_DELETED(HttpStatus.INTERNAL_SERVER_ERROR , " 파일을 삭제하려고 시도하려고 했으나 , 파일이 삭제되지 않았습니다. 다시 시도하세요."),

    ON_ENCRYPT_NO_ALGORITHM(HttpStatus.INTERNAL_SERVER_ERROR  ,   "현재 서버 환경에서 암호화가 불가능합니다. 관리자에게 문의하세요."),
    EXPIRED_TOKEN_EXCEPTION(HttpStatus.BAD_REQUEST , "jwt 토큰이 만료되었습니다.") ,
    UNSUPPORTED_JWT_EXCEPTION(HttpStatus.BAD_REQUEST , "지원하지 않는 형식의 jwt 토큰입니다.") ,
    MALFORMED_JWT_CLAIMS(HttpStatus.BAD_REQUEST ,  "잘못 서명된 jwt 토큰입니다.") ,
    ILLEGAL_JWT_EXCEPTION(HttpStatus.BAD_REQUEST ,  "jwt 토큰에 문제가 있습니다."),
    FAILED_AUTHORIZED_EXCEPTION(HttpStatus.BAD_REQUEST , "회원 확인에 실패하였습니다.") ,
    NEED_SIGN_IN_EXCEPTION(HttpStatus.BAD_REQUEST , "회원가입이 필요합니다.") ,
    NEED_LOGIN_EXCEPTION(HttpStatus.FORBIDDEN , "기능을 사용하기 위해서는 로그인이 필요합니다."),
    MISSED_AUTHORITY_ARGUMENT(HttpStatus.BAD_REQUEST, "본인인증에 필요한 내용을 정확하게 입력해주세요."),
    UNAUTHORIZED_ACCESS_EXCEPTION(HttpStatus.FORBIDDEN, "권한이 없습니다.")
    ;

    private final HttpStatus status;
    private final String statusMessage;

    ErrorCode(HttpStatus status, String statusMessage ){
        this.status = status;
        this.statusMessage = statusMessage;
    }
}
