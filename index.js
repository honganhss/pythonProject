console.log("aa");

// Load the JSON file for categories (phanloai.json)
fetch("data/phanloai.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then((categories) => {
    // Display each category in the category list
    categories.forEach((category) => {
      const listItem = document.createElement("li");
      listItem.classList.add("category-item");
      listItem.textContent = category;
      listItem.id = `${category}`;
      categoryList.appendChild(listItem);

      const divRules = document.createElement("div");
      divRules.classList.add("rules-container");
      divRules.style.display = "none";
      divRules.id = `div_${category}`;
      listItem.appendChild(divRules);

     fetch("data/association_rules.json")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          // Logic to display related rules directly
          console.log("ca: " + category);

          console.log(data)
          // Filter rules related to the selected category
          const relatedRules = data.filter((rule) => {
            const items = rule.condition.match(/\[([^\]]+)\]/)[1].split(', ').map(item => item.trim());
            // Chỉ lấy phần trước dấu '='
            const itemNames = items.map(item => item.split('=')[0].trim());
            return itemNames.includes(category);
          });

          if (relatedRules.length === 0) {
            divRules.innerHTML = `<p>Chưa có luật liên quan cho ${category}.</p>`;
          } else {
            relatedRules.forEach((rule) => {
              const ruleElement = document.createElement("div");
              ruleElement.classList.add("rule");

              // Create HTML structure for each rule
              ruleElement.innerHTML = `
                <div class="rule-header">Mặt hàng ${rule.condition}, thường được đặt cùng [${rule.result}]</div>
                <div class="rule-content">Conf: <span class="rule-confidence">${rule.confidence}</span></div>
              `;

              divRules.appendChild(ruleElement); // Append rule to the rules container
            });
          }
          // Thêm sự kiện click cho listItem
      listItem.addEventListener("click", () => {
        // Kiểm tra trạng thái hiển thị của divRules
        if (divRules.style.display === "none") {
          divRules.style.display = "block"; // Hiện divRules
        } else {
          divRules.style.display = "none"; // Ẩn divRules
        }
      });
        })
        .catch((error) => console.error("Error loading association_rules.json:", error));
     });
  })
  .catch((error) => console.error("Error loading phanloai.json:", error));
