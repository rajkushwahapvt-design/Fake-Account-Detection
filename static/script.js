const $ = (id) => document.getElementById(id);

const examples = {
  real: { username: "rahul.sharma", fullname: "Rahul Sharma", email: "rahul.sharma@gmail.com",
          bio: "CS student, Lucknow | coder",
          posts: 120, followers: 640, following: 410, profile_pic: true, external_url: false, private: false },
  fake: { username: "user83921744", fullname: "", email: "user83921744@mailinator.com",
          bio: "",
          posts: 0, followers: 4, following: 3200, profile_pic: false, external_url: true, private: false },
};

function fillExample(type) {
  const e = examples[type];
  for (const key in e) {
    const el = $(key);
    if (el.type === "checkbox") el.checked = e[key];
    else el.value = e[key];
  }
}

async function checkAccount() {
  const data = {
    username: $("username").value,
    fullname: $("fullname").value,
    email: $("email").value,
    bio: $("bio").value,
    posts: $("posts").value,
    followers: $("followers").value,
    following: $("following").value,
    profile_pic: $("profile_pic").checked ? 1 : 0,
    external_url: $("external_url").checked ? 1 : 0,
    private: $("private").checked ? 1 : 0,
  };

  const btn = $("checkBtn");
  btn.textContent = "Checking...";
  btn.disabled = true;

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const out = await res.json();
    showResult(out);
  } catch (err) {
    alert("Server se connect nahi hua. Flask chal raha hai?");
  }

  btn.textContent = "Check Account";
  btn.disabled = false;
}

function showResult(out) {
  const box = $("result");
  const isFake = out.label === "Fake";
  box.className = isFake ? "fake" : "real";

  $("verdict").textContent = isFake ? "⚠️ Likely FAKE" : "✅ Looks REAL";
  $("percent").textContent = "Fake probability: " + out.fake_probability + "%";
  $("barFill").style.width = out.fake_probability + "%";

  // risk level
  const p = out.fake_probability;
  const level = p < 30 ? "Low" : p < 70 ? "Medium" : "High";
  $("risk").textContent = "Risk level: " + level;

  // ratio
  $("ratio").textContent = "Followers/Following ratio: " + out.ratio;

  // email
  $("emailStatus").textContent = out.email
    ? (out.email.valid ? "📧 ✅ " : "📧 ❌ ") + out.email.msg
    : "";

  // reasons
  const list = $("reasons");
  list.innerHTML = "";
  const reasons = out.reasons.length ? out.reasons : ["Koi red flag nahi mila"];
  reasons.forEach((t) => {
    const li = document.createElement("li");
    li.textContent = t;
    list.appendChild(li);
  });

  box.scrollIntoView({ behavior: "smooth", block: "center" });
}