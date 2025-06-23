# 種子任務：用戶登入功能

## 任務描述
實現一個基本的用戶登入功能，作為五行AI系統的第一個協作任務。這個任務將啟動火（開發）與水（測試）的首次互動，並逐步引入其他元素。

## 任務需求

### 功能需求
1. 用戶可以使用 Line ID 登入系統
2. 系統記錄用戶的登入時間
3. 系統歡迎用戶並顯示上次登入時間
4. 支援新用戶自動註冊

### 技術需求
- 整合現有的 Line Bot 框架
- 使用記憶體存儲用戶資料（初期不需要資料庫）
- 確保程式碼清晰易讀
- 包含適當的錯誤處理

## 五行協作流程

### 第一階段：木（產品）定義需求
```json
{
  "sender": {
    "role": "產品經理",
    "element": "木",
    "timestamp": "2024-06-23T10:00:00Z"
  },
  "recipient": {
    "role": "開發專員",
    "element": "火"
  },
  "interaction_type": "相生",
  "message": {
    "type": "requirement",
    "priority": "high",
    "content": "需要實現用戶登入功能，讓AI助理能識別並記住用戶",
    "context": {
      "user_story": "作為用戶，我希望系統能記住我，這樣我就不需要每次都自我介紹",
      "acceptance_criteria": [
        "新用戶首次互動時自動註冊",
        "返回用戶看到個人化歡迎訊息",
        "顯示上次登入時間"
      ]
    }
  },
  "expected_response": "development_plan"
}
```

### 第二階段：火（開發）實作功能
```python
# 開發專員的回應
class UserLoginService:
    def __init__(self):
        self.users = {}  # {line_id: {name, last_login, created_at}}
    
    def login_or_register(self, line_id, display_name):
        """處理用戶登入或註冊"""
        current_time = datetime.now()
        
        if line_id in self.users:
            # 返回用戶
            user = self.users[line_id]
            last_login = user['last_login']
            user['last_login'] = current_time
            
            welcome_msg = f"歡迎回來，{user['name']}！\n"
            welcome_msg += f"您上次登入是在 {last_login.strftime('%Y-%m-%d %H:%M')}"
            
            return {
                "status": "login",
                "message": welcome_msg,
                "user": user
            }
        else:
            # 新用戶註冊
            self.users[line_id] = {
                "name": display_name,
                "created_at": current_time,
                "last_login": current_time
            }
            
            welcome_msg = f"歡迎新朋友 {display_name}！\n"
            welcome_msg += "我是您的AI助理，很高興認識您！"
            
            return {
                "status": "register",
                "message": welcome_msg,
                "user": self.users[line_id]
            }
```

### 第三階段：水（測試）發現問題
```json
{
  "sender": {
    "role": "測試專員",
    "element": "水",
    "timestamp": "2024-06-23T11:00:00Z"
  },
  "recipient": {
    "role": "開發專員",
    "element": "火"
  },
  "interaction_type": "相剋",
  "message": {
    "type": "bug_report",
    "priority": "high",
    "content": "發現多個問題需要修復",
    "context": {
      "issues": [
        {
          "id": "BUG001",
          "description": "display_name 可能為 None，導致程式崩潰",
          "test_case": "當用戶未設定顯示名稱時",
          "expected": "使用預設名稱或 Line ID",
          "actual": "TypeError: 'NoneType' object"
        },
        {
          "id": "BUG002",
          "description": "時間格式對台灣用戶不友善",
          "test_case": "顯示上次登入時間",
          "expected": "使用繁體中文和台灣時區",
          "actual": "英文格式，UTC時間"
        }
      ],
      "test_coverage": "基本功能測試完成，邊界案例需要加強"
    }
  },
  "expected_response": "bug_fix"
}
```

### 第四階段：土（架構）介入穩定
```json
{
  "sender": {
    "role": "架構師",
    "element": "土",
    "timestamp": "2024-06-23T12:00:00Z"
  },
  "recipient": {
    "role": "開發專員",
    "element": "火"
  },
  "interaction_type": "中性",
  "message": {
    "type": "architecture_guidance",
    "priority": "medium",
    "content": "建議重構以提高穩定性和可擴展性",
    "context": {
      "suggestions": [
        "將用戶資料抽象為 User 類別",
        "實作資料持久化介面，方便未來切換到資料庫",
        "加入設定檔管理時區和語言設定",
        "使用依賴注入模式便於測試"
      ],
      "design_pattern": "Repository Pattern + Service Layer"
    }
  },
  "expected_response": "refactoring"
}
```

### 第五階段：金（優化）精進品質
```json
{
  "sender": {
    "role": "優化專員",
    "element": "金",
    "timestamp": "2024-06-23T13:00:00Z"
  },
  "recipient": {
    "role": "測試專員",
    "element": "水"
  },
  "interaction_type": "相生",
  "message": {
    "type": "optimization_complete",
    "priority": "medium",
    "content": "完成程式碼優化，需要回歸測試",
    "context": {
      "optimizations": [
        "使用 functools.lru_cache 快取用戶查詢",
        "優化歡迎訊息生成邏輯",
        "減少不必要的時間物件創建",
        "改善錯誤訊息的可讀性"
      ],
      "performance_gain": "響應時間減少 30%",
      "code_quality": "可讀性評分從 B 提升到 A"
    }
  },
  "expected_response": "regression_test"
}
```

## 無極觀察記錄

```python
# 無極觀察者監測互動
observer = WujiObserver()

# 記錄第一次互動：木生火
observation1 = observer.observe_interaction(
    Element.WOOD, Element.FIRE, 
    "requirement", impact=1.5
)

# 記錄第二次互動：水剋火
observation2 = observer.observe_interaction(
    Element.WATER, Element.FIRE,
    "bug_report", impact=2.0
)

# 生成和諧報告
print(observer.generate_harmony_report())

# 獲取調節建議
adjustment = observer.suggest_adjustment()
if adjustment:
    print(f"建議調節：{adjustment}")
```

## 預期成果

1. **功能實現**：完整的用戶登入功能
2. **品質保證**：經過充分測試的穩定程式碼
3. **架構清晰**：可擴展的系統設計
4. **效能優良**：優化後的快速響應
5. **團隊協作**：五行元素的首次成功協作

## 學習要點

- 火與水的相剋如何促進品質提升
- 土的介入如何帶來架構穩定性
- 金的優化如何提升整體品質
- 木的需求如何驅動整個循環
- 無極如何觀察並維護系統平衡

這個種子任務將成為五行AI系統的第一個成功案例，為後續更複雜的協作奠定基礎。