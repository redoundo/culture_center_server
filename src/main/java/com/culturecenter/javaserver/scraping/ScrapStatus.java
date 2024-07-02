package com.culturecenter.javaserver.scraping;

import lombok.Getter;

import java.util.Objects;

import static com.culturecenter.javaserver.utils.Util.checking;

/**
 * 사이트에서 상태를 어떻게 표현하는지 정리해 놓은 클래스. 상태는 ING, WAIT, OVER 로 세개 존재.
 */
@Getter
public enum ScrapStatus {

    HOMEPLUS_STATUS("HOMEPLUS", "강좌 바로신청", "대기신청", "지점문의"),
    LOTTEMART_STATUS("LOTTEMART", "바로신청", "대기자 신청", "접수마감"),
    SHINSEGAE_STATUS("SHINSEGAE", "- 접수중입니다. -", "- 접수마감 되었습니다. 대기등록이 가능합니다. -", "- 접수마감 되었습니다. -"),
    HYUNDAI_STATUS("HYUNDAI", "신청 하기", "중간 신청,대기 신청", "마감"),
    GALLERIA_STATUS("GALLERIA", "접수중,마감임박", "대기접수", "접수마감"),
    LOTTE_STATUS("LOTTE", "접수중", "대기접수", "강의종료,접수마감,접수불가,지점문의"),
    EMART_STATUS("EMART", "접수중", "접수대기,정원마감", "접수마감"),
    ;

    private final String ing;
    private final String over;
    private final String wait;
    private final String center;

    ScrapStatus(String center, String ing, String wait, String over){
        this.ing = ing;
        this.over = over;
        this.wait = wait;
        this.center = center;
    }

    public String checkStatus(ScrapStatus this, String status){
        if(!checking.checkString(status)) return null;
        if(Objects.equals(status, this.getIng()) || this.getIng().indexOf(status) > 0) return "ING";
        else if (Objects.equals(status, this.getWait()) || this.getWait().indexOf(status) > 0) return "WAIT";
        else return "OVER";
    }

}
