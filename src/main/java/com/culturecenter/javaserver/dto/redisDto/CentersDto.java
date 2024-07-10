package com.culturecenter.javaserver.dto.redisDto;

import com.culturecenter.javaserver.entity.Centers;
import lombok.*;

import java.util.List;

/**
 * redis 캐싱을 진행할 때 List<Centers>.class 는 사용할 수가 없으므로 이걸 해결하기 위해 만든 dto.
 */
@Getter
@Setter
@Builder
@RequiredArgsConstructor
@AllArgsConstructor
public class CentersDto {
    private List<Centers> centers;
}
