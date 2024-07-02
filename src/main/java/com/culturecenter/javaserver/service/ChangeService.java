package com.culturecenter.javaserver.service;

import com.culturecenter.javaserver.dto.SignInInfoDto;
import com.culturecenter.javaserver.dto.UpdatableInfoDto;
import com.culturecenter.javaserver.entity.Applied;
import com.culturecenter.javaserver.entity.Liked;
import com.culturecenter.javaserver.entity.Users;
import com.culturecenter.javaserver.repository.AppliedRepository;
import com.culturecenter.javaserver.repository.LectureRepository;
import com.culturecenter.javaserver.repository.LikedRepository;
import com.culturecenter.javaserver.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import static com.culturecenter.javaserver.utils.Util.checking;

/**
 * database 데이터 변경을 진행하는 서비스
 */
@Service
@RequiredArgsConstructor
public class ChangeService {
    private final AppliedRepository appliedRepository;
    private final LikedRepository likedRepository;
    private final UserRepository userRepository;
    private final LectureRepository lectureRepository;

    /**
     * 찜한 강좌 삭제. 삭제할 강좌를 특정하지 않으면 전달된 사용자의 아이디로 저장 되어있는 찜한 강좌 전체를 삭제한다.
     * @param userId 사용자 아이디
     * @param lectureId 삭제할 강좌 아이디
     */
    @Transactional
    public void deleteLiked(Integer userId, Integer lectureId){
        if (userId != null && userId >0 && lectureId == null) {
            likedRepository.deleteAllLikedByUserId(userId);
            return;
        }
        if(userId != null && userId > 0 && lectureId > 0) likedRepository.deleteLikedByUserId(lectureId, userId);
    }

    /**
     * 지원한 내용 삭제. 삭제할 강좌를 특정하지 않으면 전달된 사용자의 아이디로 저장 되어있는 지원한 강좌 전체를 삭제한다.
     * @param userId 사용자 아이디
     * @param lectureId 삭제할 강좌 아이디
     */
    @Transactional
    public void deleteApplied(Integer userId, Integer lectureId){
        if (userId != null && userId >0 && lectureId == null) {
            appliedRepository.deleteAllAppliedByUserId(userId);
            return;
        }
        if(userId != null && userId > 0 && lectureId > 0) appliedRepository.deleteAppliedByUserId(lectureId, userId);
    }

    /**
     * 유저 정보 업데이트
     * @param userId 사용자 아이디
     * @param updatableInfo 업데이트할 정보
     */
    @Transactional
    public void updateUserInfo(Integer userId, UpdatableInfoDto updatableInfo) {
        if(updatableInfo != null && checking.checkString(updatableInfo.getNickname()) && userId > 0) {

            userRepository.updateUserInfo(updatableInfo, userId);
        }
    }
    
    @Transactional
    public void updateEnrollStatus(Integer lectureId, String status){
        if(lectureId > 0 && checking.checkString(status)) this.lectureRepository.updateEnrollStatus(lectureId, status);
    }

    /**
     * 좋아요 한 강좌 저장
     * @param userId 사용자 아이디
     * @param lectureId 강좌 아이디
     */
    @Transactional
    public void insertLikedByUserId(Integer userId, Integer lectureId) {
        if (userId > 0 && lectureId > 0) {
            Liked liked = Liked.builder()
                    .likedUserId(userId)
                    .likedLectureId(lectureId)
                    .build();
            likedRepository.save(liked);
        }
    }
    
    /**
     * 지원한 강좌 저장
     * @param userId 사용자 아이디
     * @param lectureId 강좌 아이디
     */
    @Transactional
    public void insertAppliedByUserId(Integer userId, Integer lectureId) {
        if (userId > 0 && lectureId > 0) {
            Applied applied = Applied.builder()
                    .appliedUserId(userId)
                    .appliedLectureId(lectureId)
                    .build();
            appliedRepository.save(applied);
        }
    }

    /**
     * 회원가입
     * @param signIn 회원가입 정보
     */
    @Transactional
    public Users signInUser(SignInInfoDto signIn) {
        if(checking.checkString(signIn.getNickname()) && checking.checkString(signIn.getEmail()) && checking.checkString(signIn.getPassword())){
            Users users = Users.builder()
                    .email(signIn.getEmail())
                    .password(signIn.getPassword())
                    .nickname(signIn.getNickname())
                    .snsProvider(signIn.getSnsProvider())
                    .snsProviderId(signIn.getSnsProviderId())
                    .build();
            return userRepository.save(users);
        }
        return null;
    }

    /**
     * fcm token 등록
     * @param userId 사용자 아이디
     * @param fcmToken  fcm token
     */
    @Transactional
    public void registerFcmToken(Integer userId, String fcmToken) {
        if(userId > 0  && checking.checkString(fcmToken)) userRepository.registerFcmToken(fcmToken, userId);
    }

    /**
     * 사용자 아이디로 사용자를 찾아 삭제
     * @param userId 삭제할 사용자 아이디
     */
    @Transactional
    public void deleteUserByUserId(Integer userId) {
        if(userId != null && userId > 0) userRepository.deleteById(userId);
    }

}
