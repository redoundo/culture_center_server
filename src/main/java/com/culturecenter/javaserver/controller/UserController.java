package com.culturecenter.javaserver.controller;

import com.culturecenter.javaserver.auth.AuthAnnotation;
import com.culturecenter.javaserver.dto.UpdatableInfoDto;
import com.culturecenter.javaserver.entity.Users;
import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.service.ChangeService;
import com.culturecenter.javaserver.service.SelectService;
import jakarta.annotation.security.RolesAllowed;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 로그인한 사용자 관련 요청 처리
 */
@RestController
@RequiredArgsConstructor
@RequestMapping(value = {"/api/user"})
@PreAuthorize(value = "ROLE_USER")
@RolesAllowed(value = {"USER", "ROLE_USER"})
public class UserController {
    private final ChangeService changeService;
    private final SelectService selectService;
    /**
     * 로그인 되었는지 확인. jwt 가 존재하지 않으면 front 단에서 확인해 안보내기 때문에 security 를 거쳐 진행하게끔 설정
     * @param userId 사용자 아이디
     * @return 사용자 아이디 || 에러
     */
    @GetMapping("/auth/isValid")
    @ResponseBody
    public Users isLoggedIn(@AuthAnnotation Integer userId) { 
        return this.selectService.selectUserInfo(userId, null);
    }

    /**
     * 사용자 정보 업데이트
     * @param userId 사용자 아이디
     * @param updatable 업데이트할 내용.
     * @return 사용자 정보 변경 성공 여부
     */
    @PostMapping("/myPage/edit/update")
    @ResponseBody
    public Boolean updateUserInfo(@AuthAnnotation Integer userId, @RequestBody UpdatableInfoDto updatable) {
        if (updatable == null ) return false;
        this.changeService.updateUserInfo(userId, updatable);
        return true;
    }

    /**
     * 사용자 정보 업데이트를 위해 사용자 정보를 반환
     * @param userId 사용자 아이디
     * @return 사용자 정보
     */
    @GetMapping(value = {"/myPage/edit"})
    @ResponseBody
    public Users userInfoForEditUserInfo(@AuthAnnotation Integer userId) { 
        return this.selectService.selectUserInfo(userId, null);
    }

    /**
     * 사용자 정보 및 사용자의 좋아요, 찜한 강좌 반환.
     * @param userId 사용자 아이디
     * @return 사용자 정보, 좋아요, 찜한 강좌둘.
     */
    @GetMapping("/myPage/user")
    @ResponseBody
    public Map<String, Object> userInfoAndLikedApplied(@AuthAnnotation Integer userId) { 
        return this.selectService.userInfoAndLikedApplied(userId);
    }

    /**
     * 회원탈퇴
     * @param userId 사용자 아이디
     * @return 탈퇴 성공 여부
     */
    @GetMapping("/myPage/withdraw")
    @ResponseBody
    public Boolean withdrawUser(@AuthAnnotation Integer userId) {
        this.changeService.deleteUserByUserId(userId);
        return true;
    }

    /**
     * 좋아요 혹은 지원한 강좌 삭제
     * @param userId 사용자 아이디
     * @param appliedLiked liked || applied
     * @param lectureId 삭제할 강좌 아이디
     * @return 삭제 완료 여부
     */
    @GetMapping("/myPage/{applied_liked}/delete")
    @ResponseBody
    public Boolean deleteLikedOrApplied (@AuthAnnotation Integer userId,
                                      @PathVariable("applied_liked") String appliedLiked,
                                      @RequestParam("lectureId") String lectureId) { 
        if(lectureId == null) throw  new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
        if (appliedLiked.equals("applied")) this.changeService.deleteApplied(userId, Integer.parseInt(lectureId));
        else this.changeService.deleteLiked(userId, Integer.parseInt(lectureId));
        return true;
    }

    /**
     * 좋아요한, 지원한 강좌 저장.
     * @param userId 사용자 아이디
     * @param appliedLiked applied || liked
     * @param lectureId 저장할 강좌 아이디
     * @return 저장 완료 여부
     */
    @GetMapping(value = {"/lecture/{applied_liked}", "/lecture/detail/{applied_liked}"})
    @ResponseBody
    public Boolean insertLikedOrAppliedLecture (@AuthAnnotation Integer userId,
                                             @PathVariable("applied_liked") String appliedLiked,
                                             @RequestParam("lectureId") String lectureId) { 
        if(lectureId == null) throw  new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);

        Integer IntegerLectureId = Integer.parseInt(lectureId);
        if (appliedLiked.equals("applied")) this.changeService.insertAppliedByUserId(userId, IntegerLectureId);
        else this.changeService.insertLikedByUserId(userId, IntegerLectureId);
        return true;
    }
}
