package com.culturecenter.javaserver.controller;

import com.culturecenter.javaserver.auth.JwtProvider;
import com.culturecenter.javaserver.dto.AddressFromGeoApiDto;
import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.entity.Lectures;
import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.service.SelectService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;

import static com.culturecenter.javaserver.utils.Util.checking;

import java.util.HashMap;
import java.util.Map;

/**
 * 강좌를 반환하는 컨트롤러 
 */
@Controller
@RequestMapping("/api")
@RequiredArgsConstructor
public class LectureController {
    private final SelectService selectService;
    private final JwtProvider jwtProvider;
    private final WebClient webClient = WebClient.create();

    @Value("${naver.reverse.geo.id}")
    private String naverApiId;
    @Value("${naver.reverse.geo.secret}")
    private String naverApiSecret;
    /**
     * 강좌 검색 후 및 렌더링에 필요한 내용 모두 반환.
     * @param conditions 검색 조건
     * @param token 로그인 된 경우 사용자가 좋아요 혹은 지원한 강좌도 반환하게 설정.
     * @return 렌더링에 필요한 모든 내용
     */
    @GetMapping("/lecture")
    @ResponseBody
    public Map<String, Object> searchLecturesByConditions(SearchConditions conditions, @RequestHeader(value = "Authorization", required = false) String token){
        if (conditions == null) throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);

        Map<String, Object> result = new HashMap<>();
        result.put("lectures", this.selectService.selectLectureByConditions(conditions));

        if(checking.checkString(token) && this.jwtProvider.isValid(token)) {
            Integer userId = this.jwtProvider.parseUserId(token);
            Map<String, Object> likedApplied = new HashMap<>();
            likedApplied.put("applied", this.selectService.selectAppliedByUserId(userId));
            likedApplied.put("liked", this.selectService.selectLikedByUserId(userId));
            result.put("liked_applied", likedApplied);
        } else {
            result.put("liked_applied", null);
        }

        result.put("targets", this.selectService.allTargets());
        result.put("categories", this.selectService.allCategories());
        result.put("centerTypes", this.selectService.allCenters());

        return result;
    }

    /**
     * 강좌 상세정보 가져오기
     * @param lectureId 강좌 아이디
     * @return 강좌 내용
     */
    @GetMapping("/lecture/detail")
    @ResponseBody
    public Lectures findLectureByLectureId(@RequestParam("lectureId") String lectureId) {
        if (!checking.checkString(lectureId)) throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
        return this.selectService.selectLectureByLectureId(Integer.parseInt(lectureId));
    }

    /**
     * 주소를 넘기면 위도 경도를 반환한다.
     * @param location 주소
     * @return 위도, 경도
     */
    @GetMapping("/lecture/address")
    @ResponseBody
    public AddressFromGeoApiDto findAddressByLocation(@RequestParam("location") String location) {
        String url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?coords=";
        url = url + location + "&orders=admcode&output=json";

        return this.webClient.get()
                .uri(url)
                .header("X-NCP-APIGW-API-KEY-ID", this.naverApiId)
                .header("X-NCP-APIGW-API-KEY", this.naverApiSecret)
                .retrieve()
                .bodyToMono(AddressFromGeoApiDto.class)
                .block();
    }

}
