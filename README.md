# botdiscord

# شرح السكربت:

هذا السكربت يقوم بإنشاء بوت على Discord يستخدم مكتبة `discord.py` للتفاعل مع اللاعبين في خادم MTA:SA (Multi Theft Auto: San Andreas). بالإضافة إلى ذلك، يتم استخدام Flask لإنشاء API لاستقبال الرسائل من خادم MTA وإرسالها إلى قناة على Discord.

## الوصف العام:
- البوت يقوم بتنفيذ أوامر مثل `!players` لعرض قائمة اللاعبين المتصلين، `!kick` و `!ban` لطرد اللاعبين أو حظرهم، بالإضافة إلى أوامر أخرى مثل إعطاء المال للاعبين، تحريكهم، تغيير جلدهم، وغيرها.
- كما يتم استخدام Flask لاستقبال رسائل من خادم MTA عبر HTTP POST وإرسالها إلى قناة محددة على Discord.

## كيفية استخدام السكربت:

### 1. **إعداد البوت على Discord:**
- يتم إعداد البوت باستخدام `discord.py` ويجب إضافة البوت إلى الخادم باستخدام التوكن الخاص به.
- يتم تحديد صلاحيات البوت باستخدام `commands.has_role('Admin')` للتأكد من أن الأوامر التنفيذية (مثل `!kick` و `!ban`) يمكن تنفيذها فقط بواسطة المستخدمين الذين لديهم دور "Admin".

### 2. **استخدام أوامر البوت:**
- **`!players`**: لعرض قائمة اللاعبين المتصلين في الخادم.
- **`!kick <player_name> <reason>`**: لطرد لاعب من الخادم مع تحديد السبب.
- **`!ban <player_name> <reason>`**: لحظر لاعب من الخادم مع تحديد السبب.
- **`!givemoney <player_name> <money>`**: لإعطاء لاعب مبلغ معين من المال.
- **`!setpos <player_name> <x> <y> <z>`**: لتحريك لاعب إلى موقع محدد.
- **`!getpos <player_name>`**: لعرض موقع لاعب معين.
- **`!setskin <player_name> <skin_id>`**: لتغيير جلد لاعب.
- **`!getskin <player_name>`**: لعرض جلد لاعب معين.

### 3. **استخدام Flask لاستقبال الرسائل من MTA:**
- يتم إعداد Flask لإنشاء API على العنوان `http://127.0.0.1:5000/chat` لاستقبال الرسائل من خادم MTA.
- يتم إرسال الرسائل إلى قناة Discord المحددة عند استلامها من MTA عبر POST.

### 4. **تشغيل البوت والخادم:**
- بعد إعداد الكود، يمكنك تشغيل البوت باستخدام الأمر `bot.run('token')`، مع استبدال `token` بالتوكن الخاص بالبوت.
- في نفس الوقت، يتم تشغيل خادم Flask في خيط منفصل.

### 5. **متطلبات إضافية:**
- يجب تثبيت مكتبات `discord.py`, `Flask`, و `requests` عبر:
```bash
pip install discord.py Flask requests configparser
```
### 4. **ملاحظة:**

-تأكد من أن MTA تم تكوينه بشكل صحيح في السكربت وأنك قد قمت بتعديل البيانات مثل username, password, host, و port بما يتناسب مع إعدادات خادم MTA الخاص بك.


-يوجد ملف config.ini من خلاله تستطيع تعديل كل شي تضع توكن و اسم مود والخ اهم شي يوزر نيم و باسورد يكون عنده رتبة كونسل.

-اذا تستعمل render يجب عليك ان تستعمل environment variables وتضع توكن هناك افضل لك للحمايه و يشتغل معاك  وليس من كونفق و اذا لوكال هوست عادي من كونفق 

## 5. **طريقة الاستخدام:**
يمكنك  استخدام ملف start.bat لتنزيل مشروع وبدا فيه ل ويندوز فقط.




ضع ملف s.lua و meta.xml و var.txt في ملف المودات متاع ام تي اي و ملفات باقيه للي هي config.ini scr.py lib.py updata.txt ضعها في مكان المشروع خاص بالبوت بايثون .

### 5. **خلاصة:**
-السكريبت يتيح لك التحكم الكامل في خادم MTA:SA باستخدام Discord، ويضيف مرونة في التفاعل بين الخوادم عبر API باستخدام Flask.

-حسابي علي ديسكورد ahmedly


https://wiki.multitheftauto.com/wiki/Bot_Discord
https://botdiscordmtasan.netlify.app/










