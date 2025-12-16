/speckit.constitution	Create or update project governing principles and development guidelines

1. 建立互動式網頁呈現資料分析視覺化專案
2. 前端使用vue，後端用fastapi，最後打包成exe成行檔

/speckit.specify	Define what you want to build (requirements and user stories)

1. 使用以間連線到的勁開起conda環境用名稱為fapi的環境。
2. frontend使用vue，backend用python fastapi。
3. 實作畫面美觀容易視覺化呈現的網頁，和優化的人機互動HCI功能·RWD設計，讓使用者體驗順暢
4. 要運算的資料在data/data.csv。
5. data/gxgy_transfer.ipynb是轉換公式，目前data中有gx, gy欄位，請根據轉換公視的邏輯重構程式碼，將資料中的gx, gy轉成經緯度，注意：轉換公式檔案內是經緯度轉gx, gy的參考，我要的是gx, gy轉成經緯度，請一找公式反推重構轉換程式碼。
6. 前端預設畫面開啟後要呈現一個地圖（使用前端地圖套件），在前端地圖化面呈現座標（gxgy已轉成經緯度）每個gxgy在地圖上的人數（資料欄位avg_total_users）用熱力圖呈現（使用前端地圖套件），且當滑鼠觸碰時會hover人數。
7. 資料共有四種月份（202412, 202502, 202505, 202508）欄位month，時段（0-23）欄位hour，要在地圖上呈現的熱力圖數值是分別四種月份中各個時段的數值進行輪播功能每3秒輪播。
8. 要設計月份選擇功能（四種月份），全部停留人數選擇功能欄位（avg_total_users,avg_users_under_10min,avg_users_10_30min,avg_users_over_30min），還有設計一個時間軸在地圖下方可以拉動選擇時間，如果使用者選擇了任時資料屬性及停止輪播顯示該畫面，按下輪播或重置回預設按鈕才開始輪播。
9. 根據選擇的月份時間，地圖下方同時更新性別欄位人數統計圖表（sex_1,sex_2），年齡欄位人數（age_1,age_2,age_3,age_4,age_5,age_6,age_7,age_8,age_9），年齡和性別都用百分比計算後呈現，同樣也可以做選擇。

欄位對應的中文呈現：
1,男性
2,女性
。
'1'	19歲以下
'2'	20-24歲
'3'	25-29歲
'4'	30-34歲
'5'	35-39歲
'6'	40-44歲
'7'	45-49歲
'8'	50-54歲
'9'	55-59歲
10. 確保所有資料和互動功能、更新都符合要求且正確呈現計算數值，實作高效能可維護可擴展的程式碼。

/speckit.plan	Create technical implementation plans with your chosen tech stack
/speckit.tasks	Generate actionable task lists for implementation
/speckit.implement	Execute all tasks to build the feature according to the plan

debug
1. 請檢查座標轉換的gx, gy算反了，導致轉成經緯度的座標時有錯
2. 每個點的熱力圖要依照數值大小調整顏色，不能每個點都一樣顏色，根據當前時間點地圖上的數值自動調整熱力圖
3. 將資訊欄放在左邊。地圖放在右邊
4. 停留時長的icon根據時間長短調整成可以顯示程度的icon\
5. 性別分布和年齡分佈的hover移到滑鼠正下方，顯示百分比色捨五入到小數第二位，性別分布要直接顯示百分比在下方資訊，年齡用hover就好
6. 新增平日、假日切換按鈕功能，terry_taiginyuan2.day_type欄位內容分別分為“假日” “平日”
7. 不要調整日期或時間地圖就重新縮放reload要讓切換順暢顯示數值
8. 同時全面檢查更新相關文件規格和程式碼

1. 將標題改成Data Visualization HeatMap
2. 後端啟動失敗請全面檢查