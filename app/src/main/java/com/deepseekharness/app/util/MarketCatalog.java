package com.deepseekharness.app.util;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/** 插件市场目录解析（纯逻辑，无 Android 依赖，可单测）。
 *  同时兼容两种输入：
 *  1. 内置兜底目录（tools/update-market-catalog.py 生成）：{"plugins":[{name,spec,owner,url,category,zh,en,installs,stars}]}
 *  2. deepseek1024 商店原始 API：{"packages":[{name,installMethods:[{kind,spec,verification,revision}],description:{zh,en},installCount,stars,category,owner,url}]}
 */
public final class MarketCatalog {

    public static final class Entry {
        public final String name;
        public final String spec;
        public final String owner;
        public final String url;
        public final String category;
        public final String zh;
        public final String en;
        public final int installs;
        public final int stars;

        public Entry(String name, String spec, String owner, String url, String category,
                     String zh, String en, int installs, int stars) {
            this.name = name == null ? "" : name;
            this.spec = spec == null ? "" : spec;
            this.owner = owner == null ? "" : owner;
            this.url = url == null ? "" : url;
            this.category = category == null ? "" : category;
            this.zh = zh == null ? "" : zh;
            this.en = en == null ? "" : en;
            this.installs = installs;
            this.stars = stars;
        }
    }

    private MarketCatalog() { }

    /** 解析失败或空输入一律返回空列表，不抛异常（市场降级由调用方处理）。 */
    public static List<Entry> parse(String json) {
        List<Entry> out = new ArrayList<>();
        if (json == null || json.trim().isEmpty()) return out;
        try {
            JSONObject root = new JSONObject(json);
            JSONArray slim = root.optJSONArray("plugins");
            if (slim != null) {
                for (int i = 0; i < slim.length(); i++) {
                    JSONObject p = slim.optJSONObject(i);
                    if (p == null) continue;
                    String spec = p.optString("spec", "");
                    if (spec.isEmpty()) continue;
                    out.add(new Entry(
                            p.optString("name", spec), spec,
                            p.optString("owner", ""), p.optString("url", ""),
                            p.optString("category", ""),
                            p.optString("zh", ""), p.optString("en", ""),
                            p.optInt("installs", 0), p.optInt("stars", 0)));
                }
                return out;
            }
            JSONArray raw = root.optJSONArray("packages");
            if (raw != null) {
                for (int i = 0; i < raw.length(); i++) {
                    JSONObject p = raw.optJSONObject(i);
                    if (p == null) continue;
                    String spec = pickVerifiedNpm(p.optJSONArray("installMethods"));
                    if (spec.isEmpty()) continue;
                    JSONObject desc = p.optJSONObject("description");
                    String zh = desc == null ? "" : desc.optString("zh", "");
                    String en = desc == null ? "" : desc.optString("en", "");
                    out.add(new Entry(
                            p.optString("name", spec), spec,
                            p.optString("owner", ""), p.optString("url", ""),
                            p.optString("category", ""),
                            zh, en,
                            p.optInt("installCount", 0), p.optInt("stars", 0)));
                }
            }
        } catch (Exception ignored) {
            out.clear();
        }
        return out;
    }

    /** 优先 verification=verified 的 npm spec，附加 revision 作为 @版本；逐条兜底。 */
    static String pickVerifiedNpm(JSONArray methods) {
        if (methods == null) return "";
        String fallback = "";
        for (int i = 0; i < methods.length(); i++) {
            JSONObject m = methods.optJSONObject(i);
            if (m == null) continue;
            if (!"npm".equals(m.optString("kind", ""))) continue;
            String spec = m.optString("spec", "");
            if (spec.isEmpty()) continue;
            String rev = m.optString("revision", "").trim();
            String full = rev.isEmpty() || rev.contains("@") ? spec : spec + "@" + rev;
            if ("verified".equals(m.optString("verification", ""))) return full;
            if (fallback.isEmpty()) fallback = full;
        }
        return fallback;
    }
}
