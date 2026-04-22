"""
test_agent.py
─────────────
Simple Test Agent – generates JUnit 5 tests for entity and service.

Usage:
    python test_agent.py --entity-name "Patient"
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "C:/Users/NikhilSharadMore/Downloads/demo (1)/demo"))


def generate_service_test(entity_name: str) -> str:
    """Generate JUnit 5 test for the service."""
    class_name = entity_name.capitalize()
    service_name = f"{class_name}Service"
    impl_name = f"{class_name}ServiceImpl"
    package = "com.springsequrity.demo.service"

    code = f"""package {package};

import com.springsequrity.demo.entity.{class_name};
import com.springsequrity.demo.repository.{class_name}Repository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.util.Arrays;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("{service_name} Tests")
class {impl_name}Test {{

    @Mock
    private {class_name}Repository {class_name.lower()}Repository;

    @InjectMocks
    private {impl_name} {class_name.lower()}Service;

    private {class_name} test{class_name};

    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);

        test{class_name} = new {class_name}();
        test{class_name}.setId(1);
        test{class_name}.setName("Test {class_name}");
        test{class_name}.setDescription("Test description");
    }}

    @Test
    @DisplayName("Should save {class_name}")
    void testSave{class_name}() {{
        // Arrange
        when({class_name.lower()}Repository.save(test{class_name})).thenReturn(test{class_name});

        // Act
        {class_name} result = {class_name.lower()}Service.save{class_name}(test{class_name});

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getId());
        assertEquals("Test {class_name}", result.getName());
        verify({class_name.lower()}Repository, times(1)).save(test{class_name});
    }}

    @Test
    @DisplayName("Should get all {class_name}s with pagination")
    void testGetAll{class_name}s() {{
        // Arrange
        Page<{class_name}> mockPage = new PageImpl<>(Arrays.asList(test{class_name}));
        when({class_name.lower()}Repository.findAll(PageRequest.of(0, 10))).thenReturn(mockPage);

        // Act
        Page<{class_name}> result = {class_name.lower()}Service.getAll{class_name}s(PageRequest.of(0, 10));

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getContent().size());
        verify({class_name.lower()}Repository, times(1)).findAll(PageRequest.of(0, 10));
    }}

    @Test
    @DisplayName("Should get {class_name} by ID")
    void testGet{class_name}ById() {{
        // Arrange
        when({class_name.lower()}Repository.findById(1)).thenReturn(Optional.of(test{class_name}));

        // Act
        {class_name} result = {class_name.lower()}Service.get{class_name}ById(1);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getId());
        verify({class_name.lower()}Repository, times(1)).findById(1);
    }}

    @Test
    @DisplayName("Should return null when {class_name} not found by ID")
    void testGet{class_name}ByIdNotFound() {{
        // Arrange
        when({class_name.lower()}Repository.findById(999)).thenReturn(Optional.empty());

        // Act
        {class_name} result = {class_name.lower()}Service.get{class_name}ById(999);

        // Assert
        assertNull(result);
        verify({class_name.lower()}Repository, times(1)).findById(999);
    }}

    @Test
    @DisplayName("Should delete {class_name}")
    void testDelete{class_name}() {{
        // Arrange
        doNothing().when({class_name.lower()}Repository).deleteById(1);

        // Act
        {class_name.lower()}Service.delete{class_name}(1);

        // Assert
        verify({class_name.lower()}Repository, times(1)).deleteById(1);
    }}
}}
"""
    return code


def generate_controller_test(entity_name: str) -> str:
    """Generate JUnit 5 test for the controller."""
    class_name = entity_name.capitalize()
    package = "com.springsequrity.demo.controllers"
    endpoint = f"/api/v1/{class_name.lower()}s"

    code = f"""package {package};

import com.springsequrity.demo.entity.{class_name};
import com.springsequrity.demo.service.{class_name}Service;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({class_name}Controller.class)
@DisplayName("{class_name}Controller Tests")
class {class_name}ControllerTest {{

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private {class_name}Service {class_name.lower()}Service;

    private {class_name} test{class_name};

    @BeforeEach
    void setUp() {{
        test{class_name} = new {class_name}();
        test{class_name}.setId(1);
        test{class_name}.setName("Test {class_name}");
        test{class_name}.setDescription("Test description");
    }}

    @Test
    @DisplayName("POST should create {class_name}")
    void testCreate{class_name}() throws Exception {{
        // Arrange
        String json = "{{\\\"name\\\":\\\"Test {class_name}\\\",\\\"description\\\":\\\"Test description\\\"}}";
        when({class_name.lower()}Service.save{class_name}(any())).thenReturn(test{class_name});

        // Act & Assert
        mockMvc.perform(post("{endpoint}")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists());
    }}

    @Test
    @DisplayName("GET should return all {class_name}s")
    void testGetAll{class_name}s() throws Exception {{
        // Arrange
        Page<{class_name}> mockPage = new PageImpl<>(Arrays.asList(test{class_name}));
        when({class_name.lower()}Service.getAll{class_name}s(any())).thenReturn(mockPage);

        // Act & Assert
        mockMvc.perform(get("{endpoint}")
                .param("page", "0")
                .param("size", "10")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }}

    @Test
    @DisplayName("GET by ID should return {class_name}")
    void testGet{class_name}ById() throws Exception {{
        // Arrange
        when({class_name.lower()}Service.get{class_name}ById(1)).thenReturn(test{class_name});

        // Act & Assert
        mockMvc.perform(get("{endpoint}/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1));
    }}

    @Test
    @DisplayName("GET by ID should return 404 when not found")
    void testGet{class_name}ByIdNotFound() throws Exception {{
        // Arrange
        when({class_name.lower()}Service.get{class_name}ById(999)).thenReturn(null);

        // Act & Assert
        mockMvc.perform(get("{endpoint}/999")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound());
    }}

    @Test
    @DisplayName("DELETE should remove {class_name}")
    void testDelete{class_name}() throws Exception {{
        // Arrange
        doNothing().when({class_name.lower()}Service).delete{class_name}(1);

        // Act & Assert
        mockMvc.perform(delete("{endpoint}/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNoContent());
    }}
}}
"""
    return code


def write_file(relative_path: str, content: str) -> bool:
    """Write content to a file in the project."""
    target = PROJECT_ROOT / relative_path
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"✅ Written: {relative_path}")
        return True
    except Exception as e:
        print(f"❌ Error writing {relative_path}: {e}")
        return False


def generate_tests(entity_name: str):
    """Generate and write all JUnit 5 test files."""
    print(f"\n🧪 Test Agent: Generating tests for '{entity_name}'...\n")

    # Generate Service Tests
    service_test_code = generate_service_test(entity_name)
    write_file(
        f"src/test/java/com/springsequrity/demo/service/{entity_name.capitalize()}ServiceImplTest.java",
        service_test_code
    )

    # Generate Controller Tests
    controller_test_code = generate_controller_test(entity_name)
    write_file(
        f"src/test/java/com/springsequrity/demo/controllers/{entity_name.capitalize()}ControllerTest.java",
        controller_test_code
    )

    print(f"✅ Test generation complete for '{entity_name}'!\n")


def main():
    parser = argparse.ArgumentParser(description="Unit Test Agent")
    parser.add_argument("--entity-name", required=True, help="Entity name (e.g. 'Patient')")
    args = parser.parse_args()

    generate_tests(args.entity_name)


if __name__ == "__main__":
    main()

