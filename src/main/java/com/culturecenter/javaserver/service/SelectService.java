package com.culturecenter.javaserver.service;
import com.culturecenter.javaserver.dto.LecturesInterface;
import jakarta.persistence.criteria.Predicate;
import jakarta.persistence.criteria.Root;
import jakarta.persistence.criteria.Subquery;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.entity.*;
import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.data.domain.PageRequest;
import com.culturecenter.javaserver.utils.Util;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import static com.culturecenter.javaserver.utils.Util.checking;

/**
 * database 데이터를 가져오는 서비스
 */
@Service
@RequiredArgsConstructor
public class SelectService {

    private final AppliedRepository appliedRepository;
    private final LikedRepository likedRepository;
    private final UserRepository userRepository;
    private final LectureRepository lectureRepository;
    private final CategoriesRepository categoriesRepository;
    private final CenterRepository centerRepository;
    private final TargetRepository targetRepository;

    /**
     * userId 혹은 email 을 가지고 사용자 정보를 가져온다.
     * userId || email 둘중 하나는 반드시 존재해야 한다.
     * @param userId 사용자 아이디
     * @param email 이메일
     * @return 사용자 정보
     */
    public Users selectUserInfo (Integer userId, String email){
        if (userId != null && userId > 0) {
            Optional<Users> nullableUser = userRepository.findById(userId);
            if(!nullableUser.isPresent()) throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
            else return nullableUser.get();
        }
        if(email != null && checking.checkString(email)) return userRepository.selectUserByEmail(email);
        else throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
    }

    public Map<String, Object> userInfoAndLikedApplied(Integer userId){
        if (userId == null || userId < 0) throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
        Optional<Users> nullableUser = userRepository.findById(userId);
        if(!nullableUser.isPresent()) throw new CustomRuntimeException(ErrorCode.NEED_SIGN_IN_EXCEPTION);
        Map<String , Object> map = new HashMap<>();
        Users user = nullableUser.get();
        map.put("user", user);
        map.put("applied", this.appliedRepository.allLectureByUserId(userId));
        map.put("liked", this.likedRepository.allLectureByUserId(userId));
        return map;
    }

    /**
     * 사용자 아이디로 찜한 강좌들 가져오기
     * @param userId 사용자 아이디
     * @return 짐핸 강좌 내역
     */
    public List<LecturesInterface> selectLikedByUserId (Integer userId) {
        if(userId != null && userId > 0) return likedRepository.allLectureByUserId(userId);
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 사용자 아이디로 지원한 강좌들 가져오기
     * @param userId 사용자 아이디
     * @return 지원한 강좌 내역
     */
    public List<LecturesInterface> selectAppliedByUserId (Integer userId) {
        if (userId != null && userId > 0) return appliedRepository.allLectureByUserId(userId);
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 유효한 닉네임인지 확인
     * @param nickname 닉네임
     * @return 유효성 여부
     */
    public Boolean checkNicknameUniqueness (String nickname) {
        if(checking.checkString(nickname)) return userRepository.checkNicknameUniqueness(nickname);
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 이메일로 사용자가 이미 존재하는지 확인
     * @param email 이메일
     * @return 존재 여부
     */
    public Boolean checkUserExist (String email, String sns) {
        if(checking.checkString(email)) {
            if (sns.equals("CultureCenters")) return userRepository.checkCultureCenterUserExist(email);
            else return userRepository.checkUserExist(email);
        }
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 모든 카테고리 반환
     * @return 카테고리들
     */
    public List<Categories> allCategories () {
        return categoriesRepository.findAll();
    }

    /**
     * 모든 대상 반환
     * @return 대상들
     */
    public List<Targets> allTargets () {
        return targetRepository.findAll();
    }

    /**
     * 모든 기관 반환.
     * @return 기관들.
     */
    public List<Centers> allCenters() {
        return centerRepository.findAll();
    }

    /**
     * 특정 타입의 센터 반환
     * @param type 타입
     * @return 해당 타입의 센터 정보
     */
    public List<Centers> centerByType(String type) {
        if (type != null && checking.checkString(type)) return centerRepository.selectCentersByType(type);
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 강좌 내용 가져오기
     * @param lectureId 강좌 아이디
     * @return 강좌 내용
     */
    public Lectures selectLectureByLectureId (Integer lectureId) {
        if(lectureId != null && lectureId > 0) {
            Optional<Lectures> optionalLectures = lectureRepository.findById(lectureId);
            if(optionalLectures.isPresent()) return optionalLectures.get();
            else throw new CustomRuntimeException(ErrorCode.NO_SUCH_DATA_ERROR);
        }
        else throw new CustomRuntimeException(ErrorCode.MISSING_CONTENT_ERROR);
    }

    /**
     * 검색 조건으로 강좌를 조회한 뒤 반환한다.
     * @param conditions 검색 조건
     * @return 강좌 내용
     */
    public List<Lectures> selectLectureByConditions (SearchConditions conditions) {
        Pageable pageable = PageRequest.of(conditions.getPage() == null ? 1 : (conditions.getPage() - 1) * 16 + 1, 16);
        Specification<Lectures> spec = (root, query, criteriaBuilder) -> {
            Predicate predicate = criteriaBuilder.conjunction();
            // 대상 설정만 존재 할 때는 null 이 아니면 가져오게 한다.
            if (checking.checkString(conditions.getTarget()) && !checking.checkString(conditions.getCategory()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.isNotNull(root.get(conditions.getTarget())));
            // 대상과 카테고리 둘다 있을 경우에는 해당 대상이 찾으려는 카테고리를 가지고 있을 경우에만 가져온다.
            if (checking.checkString(conditions.getCategory()) && checking.checkString(conditions.getTarget()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.equal(root.get(conditions.getTarget()), conditions.getCategory()));
            if (checking.checkString(conditions.getKeyword()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.equal(root.get("title"), "%" + conditions.getKeyword() + "%"));
            if (checking.checkString(conditions.getCenterType()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.equal(root.get("type"), conditions.getCenterType()));
            if (checking.checkString(conditions.getCenterName()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.equal(root.get("center"), conditions.getCenterName()));
            if (checking.checkString(conditions.getAddress()))
                predicate = criteriaBuilder.and(predicate, criteriaBuilder.equal(root.get("address"), "%" + conditions.getAddress() + "%"));
            if (conditions.getLatitude() != null && conditions.getLongitude() != null){
                Subquery<String> subquery = query.subquery(String.class);
                Root<Branches> branchesRoot = subquery.from(Branches.class);
                Util util = new Util();
                double[] lonAndLat = util.calculateLocation(conditions.getLatitude(), conditions.getLongitude(), 300);
                subquery.select(branchesRoot.get("branchName"))
                        .where(criteriaBuilder.between(branchesRoot.get("latitude"), lonAndLat[0], lonAndLat[1]))
                        .where(criteriaBuilder.between(branchesRoot.get("longitude"), lonAndLat[2], lonAndLat[3]));
                predicate = criteriaBuilder.and(predicate, root.get("branch").in(subquery));
            }
            return predicate;
        };
        return lectureRepository.findAll(spec, pageable).stream().toList();
    }
}
