# API Request Format Verification

## ✅ **Authentication Endpoints - VERIFIED**

### 1. Send Login OTP
**Endpoint:** `POST /api/v1/auth/login/send-otp`
**Schema:** `OTPLoginSendRequest`
```json
{
  "phone_number": "string" // ✅ CORRECT
}
```

### 2. Verify Login OTP  
**Endpoint:** `POST /api/v1/auth/login/verify-otp`
**Schema:** `OTPLoginVerifyRequest`
```json
{
  "phone_number": "string", // ✅ CORRECT
  "otp_code": "string"      // ✅ CORRECT (4-8 chars)
}
```

### 3. Send Signup OTP
**Endpoint:** `POST /api/v1/auth/signup/send-otp`
**Schema:** `OTPSignupSendRequest`
```json
{
  "phone_number": "string" // ✅ CORRECT
}
```

### 4. Verify Signup OTP
**Endpoint:** `POST /api/v1/auth/signup/verify-otp`
**Schema:** `OTPSignupVerifyRequest`
```json
{
  "phone_number": "string",        // ✅ CORRECT
  "otp_code": "string",           // ✅ CORRECT (4-8 chars)
  "name": "string",               // ✅ CORRECT (1-100 chars)
  "email": "string|null",         // ✅ OPTIONAL
  "password": "string",           // ✅ CORRECT (min 8 chars)
  "has_given_consent": boolean    // ✅ CORRECT (required)
}
```

## ⚠️ **Records Endpoints - NEEDS VERIFICATION**

### 5. Create Record
**Endpoint:** `POST /api/v1/records/`
**Schema:** `RecordCreate`
```json
{
  "title": "string",              // ✅ CORRECT (1-200 chars)
  "description": "string|null",   // ✅ CORRECT (max 1000 chars)
  "media_type": "MediaType",      // ✅ CORRECT (text|audio|video|image|document)
  "release_rights": "ReleaseRights", // ⚠️ CHECK: creator|family_or_friend|downloaded|NA
  "language": "Language",         // ✅ CORRECT (enum values)
  "user_id": "uuid",             // ✅ CORRECT
  "category_id": "uuid",         // ✅ CORRECT
  "location": "Coordinates|null"  // ✅ OPTIONAL
}
```

### 6. Upload Chunk
**Endpoint:** `POST /api/v1/records/upload/chunk`
**Content-Type:** `multipart/form-data`
```json
{
  "chunk": "binary",        // ✅ CORRECT
  "filename": "string",     // ✅ CORRECT
  "chunk_index": "integer", // ✅ CORRECT
  "total_chunks": "integer", // ✅ CORRECT
  "upload_uuid": "string"   // ✅ CORRECT
}
```

### 7. Upload Record (Finalize)
**Endpoint:** `POST /api/v1/records/upload`
**Content-Type:** `application/x-www-form-urlencoded`
```json
{
  "title": "string",
  "description": "string|null",
  "category_id": "string",
  "user_id": "string",
  "media_type": "MediaType",
  "upload_uuid": "string",
  "filename": "string", 
  "total_chunks": "integer",
  "latitude": "number|null",
  "longitude": "number|null",
  "release_rights": "ReleaseRights", // ⚠️ CHECK VALUES
  "language": "Language"
}
```

## 🎨 **Swecha UI Analysis**

### **Categories from Swecha Example:**
1. **Fables** 📚 - Traditional stories with moral lessons
2. **Events** 🎉 - Happenings, celebrations, and special occasions  
3. **Music** 🎵 - Musical content, songs, instruments
4. **Places** 🏛️ - Locations, landmarks, and geographical content
5. **Food** 🍽️ - Culinary content, recipes, and food-related information
6. **People** 👥 - Individuals, personalities, and human-related content
7. **Literature** 📖 - Books, poems, writings, and literary works
8. **Architecture** 🏗️ - Buildings, structures, and architectural designs
9. **Skills** ⚡ - Abilities, talents, and learning resources
10. **Images** 🖼️ - Visual content, pictures, and graphic materials
11. **Culture** 🎭 - Cultural traditions, customs, and heritage
12. **Flora & Fauna** 🌿 - Plants, animals, and natural life forms
13. **Education** 🎓 - Learning materials, courses, and educational content
14. **Vegetation** 🌱 - Plant life, gardening, and botanical content
15. **Folk Tales** 📓 - Stories passed orally across generations
16. **Folk Songs** 🎶 - Traditional music reflecting cultural heritage
17. **Traditional Skills** 🛠️ - Local artisanal and craft practices
18. **Local Cultural History** 🏛️ - Cultural events, rituals, and customs
19. **Local History** 📜 - Historical events and figures significant to region
20. **Food & Agriculture** 🌾 - Traditional recipes, cooking methods, practices
21. **Newspapers Older Than 1980s** 📰 - From libraries or archives

### **UI/UX Features from Swecha:**
- **Gradient Header**: Purple gradient with white text
- **Card Layout**: Rounded cards with hover effects and scale animation
- **Grid System**: Responsive grid (1-4 columns based on screen size)
- **Clean Typography**: Clear hierarchy with emoji, title, description
- **Hover Effects**: Scale transform and shadow changes
- **User Actions**: Profile and logout buttons in header
- **Modern Design**: Clean, minimal, professional appearance

## 🔧 **Required Updates:**

1. **Fix release_rights mapping** - Check enum values
2. **Update categories** to match Swecha's 21 categories
3. **Improve UI styling** to match Swecha's modern design
4. **Add proper form validation** for all required fields