package com.deepseekharness.app.util;

import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class MarketCatalogTest {

    @Test
    public void parsesBundledSlimFormat() {
        String json = "{\"plugins\":[{\"name\":\"远程 UI\",\"spec\":\"dsh-remote-ui@0.6.5\","
                + "\"owner\":\"mrRisega\",\"url\":\"https://github.com/mrRisega/dsh-remote\","
                + "\"category\":\"ui\",\"zh\":\"远程界面\",\"en\":\"Remote UI\",\"installs\":7,\"stars\":56}]}";
        List<MarketCatalog.Entry> list = MarketCatalog.parse(json);
        assertEquals(1, list.size());
        MarketCatalog.Entry e = list.get(0);
        assertEquals("dsh-remote-ui@0.6.5", e.spec);
        assertEquals("远程界面", e.zh);
        assertEquals(7, e.installs);
    }

    @Test
    public void parsesRawApiAndPrefersVerifiedNpm() {
        String json = "{\"packages\":[{\"name\":\"x\",\"installCount\":3,\"stars\":9,"
                + "\"description\":{\"zh\":\"描述\",\"en\":\"desc\"},"
                + "\"installMethods\":["
                + "{\"kind\":\"github\",\"spec\":\"github:a/b\",\"verification\":\"verified\"},"
                + "{\"kind\":\"npm\",\"spec\":\"pkg-x\",\"revision\":\"1.2.0\",\"verification\":\"verified\"},"
                + "{\"kind\":\"npm\",\"spec\":\"pkg-y\",\"revision\":\"0.0.1\",\"verification\":\"unverified\"}]}]}";
        List<MarketCatalog.Entry> list = MarketCatalog.parse(json);
        assertEquals(1, list.size());
        assertEquals("pkg-x@1.2.0", list.get(0).spec);
        assertEquals("描述", list.get(0).zh);
    }

    @Test
    public void fallsBackToUnverifiedNpmWhenNoVerified() {
        String json = "{\"packages\":[{\"name\":\"y\","
                + "\"installMethods\":[{\"kind\":\"npm\",\"spec\":\"only-pkg\",\"revision\":\"0.1.0\","
                + "\"verification\":\"unverified\"}]}]}";
        List<MarketCatalog.Entry> list = MarketCatalog.parse(json);
        assertEquals(1, list.size());
        assertEquals("only-pkg@0.1.0", list.get(0).spec);
    }

    @Test
    public void emptyAndGarbageInputReturnEmptyList() {
        assertTrue(MarketCatalog.parse(null).isEmpty());
        assertTrue(MarketCatalog.parse("").isEmpty());
        assertTrue(MarketCatalog.parse("not json").isEmpty());
        assertTrue(MarketCatalog.parse("{}").isEmpty());
    }

    @Test
    public void entriesWithoutSpecAreSkipped() {
        String json = "{\"plugins\":[{\"name\":\"无spec\"},{\"name\":\"有\",\"spec\":\"ok@1.0.0\"}]}";
        List<MarketCatalog.Entry> list = MarketCatalog.parse(json);
        assertEquals(1, list.size());
        assertEquals("ok@1.0.0", list.get(0).spec);
    }
}
