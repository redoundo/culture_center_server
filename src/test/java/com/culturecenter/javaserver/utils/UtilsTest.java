package com.culturecenter.javaserver.utils;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.dto.redisDto.CategoriesDto;
import com.culturecenter.javaserver.entity.Categories;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.util.ArrayList;
import java.util.List;

import static com.culturecenter.javaserver.utils.Util.checking;
import static org.junit.jupiter.api.Assertions.*;


@DisplayName("유틸리티 테스트")
public class UtilsTest {

    @Test
    @Disabled
    @DisplayName("리플렉션을 이용해 두 객체의 내용과 타입이 동일한지 확인 해본다.")
    public void reflectionTest() {

        SearchConditions conditions1 = SearchConditions
                .builder()
                .centerName("HOMEPLUS")
                .build();
        SearchConditions conditions2 = SearchConditions
                .builder()
                .centerName("EMART")
                .page(1)
                .build();

        boolean same = checking.sameContentObject(conditions2, conditions1);
        assertFalse(same);
    }

    @Test
    @Disabled
    @DisplayName("다양한 타입을 오류 없이 json 으로 바꾸거나 자바 객체로 바꾸는지 확인")
    public void objectToJsonToObjectTest() {

        SearchConditions conditions = SearchConditions
                .builder()
                .centerName("EMART")
                .page(1)
                .build();

        Categories category = Categories
                .builder()
                .categoryId(1)
                .categoryName("adult")
                .targetId(1)
                .build();
        List<Categories> categories = new ArrayList<>();
        categories.add(category);
        CategoriesDto dto = CategoriesDto.builder().categories(categories).build();

        String objToStr = checking.javaObjectToJson(conditions);
        String categoryToStr = checking.javaObjectToJson(dto);

        CategoriesDto categoriesDto = checking.jsonToJavaObject(categoryToStr, CategoriesDto.class);
        SearchConditions conditions1 = checking.jsonToJavaObject(objToStr, SearchConditions.class);

        assertTrue(checking.sameContentObject(conditions, conditions1));
        assertTrue(checking.sameContentObject(dto, categoriesDto));
    }

    @Test
    @DisplayName("비밀번호 변경 테스트")
    @Disabled
    void encryptTest() {
        String password = "password";
        BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
        String encryptedPassword = passwordEncoder.encode(password);
        System.out.println(encryptedPassword);
        assertNotNull(encryptedPassword);
    }
}
