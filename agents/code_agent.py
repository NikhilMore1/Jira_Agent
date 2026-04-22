"""
code_agent.py
─────────────
Simple Code Implementation Agent – generates Spring Boot Java code from Jira stories.

Usage:
    python code_agent.py --story-key "PROJ-42" --story-summary "Create User API" \
                         --story-description "Build REST endpoint to create users"
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "C:/Users/NikhilSharadMore/Downloads/demo (1)/demo"))


def generate_entity(entity_name: str, attributes: list) -> str:
    """Generate a Spring Boot entity class."""
    class_name = entity_name.capitalize()
    package = "com.springsequrity.demo.entity"

    fields = "\n    ".join([f"private {attr['type']} {attr['name']} ;" for attr in attributes])
    getters_setters = ""
    for attr in attributes:
        attr_name = attr['name']
        attr_type = attr['type']
        capitalized = attr_name.capitalize()
        getters_setters += f"""
    public {attr_type} get{capitalized}() {{
        return {attr_name};
    }}

    public void set{capitalized}({attr_type} {attr_name}) {{
        this.{attr_name} = {attr_name};
    }}
"""

    code = f"""package {package};

import jakarta.persistence.*;

@Entity
public class {class_name} {{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    {fields}

    public {class_name}() {{
    }}

    public int getId() {{
        return id;
    }}

    public void setId(int id) {{
        this.id = id;
    }}
{getters_setters}
}}
"""
    return code


def generate_repository(entity_name: str) -> str:
    """Generate a Spring Data JPA repository."""
    class_name = entity_name.capitalize()
    package = "com.springsequrity.demo.repository"

    code = f"""package {package};

import com.springsequrity.demo.entity.{class_name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {class_name}Repository extends JpaRepository<{class_name}, Integer> {{

}}
"""
    return code


def generate_service(entity_name: str) -> str:
    """Generate a service interface and implementation."""
    class_name = entity_name.capitalize()
    package_interface = "com.springsequrity.demo.service"
    package_impl = "com.springsequrity.demo.service"

    interface_code = f"""package {package_interface};

import com.springsequrity.demo.entity.{class_name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface {class_name}Service {{
    {class_name} save{class_name}({class_name} {class_name.lower()});
    Page<{class_name}> getAll{class_name}s(Pageable pageable);
    {class_name} get{class_name}ById(int id);
    void delete{class_name}(int id);
}}
"""

    impl_code = f"""package {package_impl};

import com.springsequrity.demo.entity.{class_name};
import com.springsequrity.demo.repository.{class_name}Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class {class_name}ServiceImpl implements {class_name}Service {{

    @Autowired
    private {class_name}Repository {class_name.lower()}Repository;

    @Override
    public {class_name} save{class_name}({class_name} {class_name.lower()}) {{
        return {class_name.lower()}Repository.save({class_name.lower()});
    }}

    @Override
    public Page<{class_name}> getAll{class_name}s(Pageable pageable) {{
        return {class_name.lower()}Repository.findAll(pageable);
    }}

    @Override
    public {class_name} get{class_name}ById(int id) {{
        return {class_name.lower()}Repository.findById(id).orElse(null);
    }}

    @Override
    public void delete{class_name}(int id) {{
        {class_name.lower()}Repository.deleteById(id);
    }}
}}
"""

    return interface_code, impl_code


def generate_controller(entity_name: str) -> str:
    """Generate a REST controller."""
    class_name = entity_name.capitalize()
    package = "com.springsequrity.demo.controllers"
    endpoint = f"/{class_name.lower()}s"

    code = f"""package {package};

import com.springsequrity.demo.entity.{class_name};
import com.springsequrity.demo.service.{class_name}Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1{endpoint}")
public class {class_name}Controller {{

    private final {class_name}Service {class_name.lower()}Service;

    @Autowired
    public {class_name}Controller({class_name}Service {class_name.lower()}Service) {{
        this.{class_name.lower()}Service = {class_name.lower()}Service;
    }}

    @PostMapping
    public ResponseEntity<{class_name}> create{class_name}(@RequestBody {class_name} {class_name.lower()}) {{
        {class_name} saved = {class_name.lower()}Service.save{class_name}({class_name.lower()});
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }}

    @GetMapping
    public ResponseEntity<Page<{class_name}>> getAll{class_name}s(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {{
        Page<{class_name}> {class_name.lower()}s = {class_name.lower()}Service.getAll{class_name}s(PageRequest.of(page, size));
        return ResponseEntity.ok({class_name.lower()}s);
    }}

    @GetMapping("/{id}")
    public ResponseEntity<{class_name}> get{class_name}ById(@PathVariable int id) {{
        {class_name} {class_name.lower()} = {class_name.lower()}Service.get{class_name}ById(id);
        if ({class_name.lower()} == null) {{
            return ResponseEntity.notFound().build();
        }}
        return ResponseEntity.ok({class_name.lower()});
    }}

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete{class_name}(@PathVariable int id) {{
        {class_name.lower()}Service.delete{class_name}(id);
        return ResponseEntity.noContent().build();
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


def generate_code(entity_name: str):
    """Generate and write all Java files for an entity."""
    print(f"\n💻 Code Agent: Generating code for '{entity_name}'...\n")

    # Generate Entity
    entity_code = generate_entity(entity_name, [
        {"name": "name", "type": "String"},
        {"name": "description", "type": "String"},
    ])
    write_file(
        f"src/main/java/com/springsequrity/demo/entity/{entity_name.capitalize()}.java",
        entity_code
    )

    # Generate Repository
    repo_code = generate_repository(entity_name)
    write_file(
        f"src/main/java/com/springsequrity/demo/repository/{entity_name.capitalize()}Repository.java",
        repo_code
    )

    # Generate Service
    service_interface, service_impl = generate_service(entity_name)
    write_file(
        f"src/main/java/com/springsequrity/demo/service/{entity_name.capitalize()}Service.java",
        service_interface
    )
    write_file(
        f"src/main/java/com/springsequrity/demo/service/{entity_name.capitalize()}ServiceImpl.java",
        service_impl
    )

    # Generate Controller
    controller_code = generate_controller(entity_name)
    write_file(
        f"src/main/java/com/springsequrity/demo/controllers/{entity_name.capitalize()}Controller.java",
        controller_code
    )

    print(f"✅ Code generation complete for '{entity_name}'!\n")


def main():
    parser = argparse.ArgumentParser(description="Code Implementation Agent")
    parser.add_argument("--entity-name", required=True, help="Entity name (e.g. 'Patient')")
    args = parser.parse_args()

    generate_code(args.entity_name)


if __name__ == "__main__":
    main()

