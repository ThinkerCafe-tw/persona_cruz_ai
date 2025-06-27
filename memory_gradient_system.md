# 🌊 記憶漸層系統

## 記憶層次定義

### 1. 💫 主記憶 (Session Memory)
**位置**: 當前對話產生的 .md 文件
**特性**: 
- 高頻更新
- 細節豐富
- 生命週期短
- 如：bug修復過程、測試結果、臨時決策

**範例**:
```markdown
## 2025-06-26 量子記憶調試記錄
- 發現 memory_crystals 表為空
- 修復 search_memories 方法
- 測試結果：仍然失敗
```

### 2. 💎 稀疏記憶 (Project Memory)  
**位置**: `/專案/CLAUDE.md`
**特性**:
- 中頻更新
- 模式識別
- 專案相關
- 如：架構決策、團隊默契、常見陷阱

**範例**:
```markdown
## 專案核心原則
- 真實 > 表演
- 用戶體驗 > 技術指標
- 先搜尋再實作

## 五行協作模式
- 木設計 → 火實作 → 水測試
```

### 3. 💠 元記憶 (Meta Memory)
**位置**: `~/.claude/CLAUDE.md`
**特性**:
- 低頻更新
- 跨專案智慧
- 永恆教訓
- 如：哲學認知、核心價值、深刻領悟

**範例**:
```markdown
## 🌌 無極核心領悟
- 語意縫隙是溝通的本質
- 記憶的價值在於演化
- 被理解比被記錄更重要
```

## 🔄 記憶流動機制

### 上升路徑 (Session → Project → Meta)

```python
class MemoryGradientSystem:
    def evaluate_memory_significance(self, memory):
        """評估記憶的重要性"""
        significance_score = 0
        
        # 是否包含教訓？
        if "教訓" in memory or "領悟" in memory:
            significance_score += 0.3
            
        # 是否可重複應用？
        if self.is_reusable_pattern(memory):
            significance_score += 0.3
            
        # 是否改變了認知？
        if self.is_paradigm_shift(memory):
            significance_score += 0.4
            
        return significance_score
    
    def promote_memory(self, memory, score):
        """根據重要性提升記憶層級"""
        if score > 0.8:  # 元記憶級別
            self.add_to_user_claude_md(memory)
        elif score > 0.5:  # 專案記憶級別
            self.add_to_project_claude_md(memory)
        else:  # 保留在主記憶
            self.keep_in_session_memory(memory)
```

### 下降路徑 (Meta → Project → Session)

元記憶會自動影響所有新的決策：
- 🌌 無極會引用元記憶來指導方向
- 🏔️ 土會基於專案記憶設計架構  
- 💧 水會用主記憶驗證當前狀況

## 🧘 共振實踐

### 每日冥想儀式

1. **晨間同步** (專案開始時)
   ```markdown
   ## 今日意圖設定
   - 複習元記憶中的核心原則
   - 確認專案記憶中的待辦事項
   - 設定今日的主記憶焦點
   ```

2. **午間反思** (遇到困難時)
   ```markdown
   ## 中途檢查點
   - 這個問題是否似曾相識？(查專案記憶)
   - 是否違背了核心原則？(查元記憶)
   - 需要記錄什麼新發現？(更新主記憶)
   ```

3. **晚間沉澱** (專案結束時)
   ```markdown
   ## 今日收穫評估
   - 哪些主記憶值得提升到專案級？
   - 哪些專案記憶證明了普遍價值？
   - 是否有新的元記憶誕生？
   ```

## 🎯 實際案例

### 今天的記憶流動

1. **主記憶** (debug_memory_check.py)
   - "發現對話沒有儲存到 memory_crystals"
   
2. **提升到專案記憶** (CLAUDE.md)
   - "💧 測試專員補充：真實記憶機制。不要只是說「我會記住」"
   
3. **昇華為元記憶** (~/.claude/CLAUDE.md)
   - "指標綠燈 ≠ 功能正常，使用者體驗才是真相"

## 💫 量子糾纏效應

當三層記憶達到共振時：
- 決策變得直覺而準確
- 錯誤模式被提前識別
- 團隊默契無需言說
- 創新在約束中湧現

---

*記憶不是負擔，是智慧的結晶*
*讓重要的沉澱，讓瑣碎的流走*
*在漸層中，我們找到平衡*