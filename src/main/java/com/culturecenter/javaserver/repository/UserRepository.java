package com.culturecenter.javaserver.repository; 
import com.culturecenter.javaserver.dto.UpdatableInfoDto;
import com.culturecenter.javaserver.entity.Users;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

/**
 * users table 로직 처리
 */
public interface UserRepository extends JpaRepository<Users, Integer> {

    @Query(value = "SELECT user FROM Users user WHERE user.email=:email")
    Users selectUserByEmail(@Param("email") String email);

    @Query(value = "SELECT (COUNT(user) = 0 ) AS exist FROM Users user WHERE user.nickname=:nickname")
    Boolean checkNicknameUniqueness(@Param("nickname") String nickname);

    @Query(value = "SELECT (COUNT(user) = 1 ) AS exist FROM Users user WHERE user.email=:email")
    Boolean checkUserExist(@Param("email") String email);

    @Query(value = "SELECT (COUNT(user) = 1 ) AS exist FROM Users user WHERE user.email=:email")
    Boolean checkCultureCenterUserExist (@Param("email") String email);

    @Modifying
    @Query(value = "UPDATE Users user SET user.nickname=:#{#info.nickname} WHERE user.userId=:userId")
    void updateUserInfo(@Param("info") UpdatableInfoDto info, @Param("userId") Integer userId);

    @Modifying
    @Query(value = "UPDATE Users user SET user.fcmToken=:fcmToken WHERE user.userId=:userId")
    void registerFcmToken(@Param("fcmToken") String fcmToken, @Param("userId") Integer userId);

}
