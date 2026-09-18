package com.deepseekharness.app.util;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** 单测辅助：本机工具链（SDK 36 + JDK 21）下 Files.readString/writeString 对
 *  javac 不可见（bootclasspath 组合导致 ct.sym 按 Java 8 API 视图解析）。
 *  用 Java 7 API 等价实现，行为一致。 */
public final class TestIo {

    private TestIo() { }

    public static String readText(Path path) throws IOException {
        return new String(Files.readAllBytes(path), StandardCharsets.UTF_8);
    }

    public static void writeText(Path path, String content) throws IOException {
        Files.write(path, content.getBytes(StandardCharsets.UTF_8));
    }
}
