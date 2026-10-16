import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات

QUESTIONS_DB = {
  "مبتدئ": [
           {
             "id": 1,
        "type": "multiple-choice",
        "prompt": "المكان الذي نتعلم فيه ويعتبر بيتنا الثاني هو:",
        "options": ["المستشفى", "النادي", "المدرسة", "السوق"],
        "answer": "المدرسة"
    },
    {
        "id": 2,
        "type": "multiple-choice",
        "prompt": "المسئول عن تصميم وبناء المنازل والمدارس والمباني الجميلة هو:",
        "options": ["المعلم", "المهندس", "الطبيب", "المزارع"],
        "answer": "المهندس"
    },
    {
        "id": 3,
        "type": "multiple-choice",
        "prompt": "إذا أردنا وصف مكان ما مثل المنزل أو المدرسة بدقة، يمكننا رسم:",
        "options": ["لوحة زيتية", "مخطط مصغر", "صورة فوتوغرافية", "مجسم زجاجي"],
        "answer": "مخطط مصغر"
    },
    {
        "id": 4,
        "type": "multiple-choice",
        "prompt": "رسم مخطط مصغر للمكان كأننا نراه من الأعلى يساعد على معرفة تفاصيل المكان بطريقة أوضح من:",
        "options": ["الوصف بالكلمات", "الألوان الزاهية", "التصوير اللامع", "الرسم الهندسي"],
        "answer": "الوصف بالكلمات"
    },
    {
        "id": 5,
        "type": "multiple-choice",
        "prompt": "عند رسم المهندس للمخطط، يتم مراعاة رسم الشمس في أي مكان؟",
        "options": ["داخل المنزل", "خارج المنزل", "تحت المنزل", "داخل الغرف"],
        "answer": "خارج المنزل"
    },
    {
        "id": 6,
        "type": "multiple-choice",
        "prompt": "يتم إضافة الأبواب والنوافذ في مخطط المبنى لتسمح بدخول الهواء و:",
        "options": ["المطر", "الأثاث", "ضوء الشمس", "الأصدقاء"],
        "answer": "ضوء الشمس"
    },
    {
        "id": 7,
        "type": "multiple-choice",
        "prompt": "تخرج الشمس دائماً كل صباح من اتجاه:",
        "options": ["الشمال", "الجنوب", "الشرق", "الغرب"],
        "answer": "الشرق"
    },
    {
        "id": 8,
        "type": "multiple-choice",
        "prompt": "عدد الاتجاهات الأصلية هو:",
        "options": ["ثلاثة اتجاهات", "أربعة اتجاهات", "خمسة اتجاهات", "ستة اتجاهات"],
        "answer": "أربعة اتجاهات"
    },
    {
        "id": 9,
        "type": "multiple-choice",
        "prompt": "أحد الاتجاهات التالية يُعد من الاتجاهات الأصلية:",
        "options": ["الشمال الشرقي", "الجنوب الغربي", "الجنوب", "الشمال الغربي"],
        "answer": "الجنوب"
    },
    {
        "id": 10,
        "type": "multiple-choice",
        "prompt": "يوجد بين كل اتجاهين أصليين اتجاه:",
        "options": ["حقيقي", "فرعي", "رئيسي", "مستقيم"],
        "answer": "فرعي"
    },
    {
        "id": 11,
        "type": "multiple-choice",
        "prompt": "الاتجاه الفرعي الذي يقع بين اتجاه الشمال واتجاه الشرق هو:",
        "options": ["الشمال الشرقي", "الشمال الغربي", "الجنوب الشرقي", "الجنوب الغربي"],
        "answer": "الشمال الشرقي"
    },
    {
        "id": 12,
        "type": "multiple-choice",
        "prompt": "الاتجاه الجنوبي الغربي يقع بين اتجاه الجنوب واتجاه:",
        "options": ["الشمال", "الشرق", "الغرب", "الشمال الشرقي"],
        "answer": "الغرب"
    },
    {
        "id": 13,
        "type": "multiple-choice",
        "prompt": "الجهة المقابلة لاتجاه الغرب تكون جهة:",
        "options": ["الشمال", "الجنوب", "الشرق", "الشمال الغربي"],
        "answer": "الشرق"
    },
    {
        "id": 14,
        "type": "multiple-choice",
        "prompt": "الجهة المقابلة لاتجاه الجنوب هي جهة:",
        "options": ["الشمال", "الشرق", "الغرب", "الجنوب الشرقي"],
        "answer": "الشمال"
    },
    {
        "id": 15,
        "type": "multiple-choice",
        "prompt": "الاتجاه الفرعي المقابل لاتجاه الشمال الغربي هو:",
        "options": ["الشمال الشرقي", "الجنوب الشرقي", "الجنوب الغربي", "الشمال"],
        "answer": "الجنوب الشرقي"
    },
    {
        "id": 16,
        "type": "multiple-choice",
        "prompt": "اعتمد الإنسان قديماً على الطبيعة لتحديد الاتجاهات مستخدماً وسائل متعددة منها النجوم و:",
        "options": ["البوصلة", "الشمس", "الهواتف الذكية", "الخرائط الرقمية"],
        "answer": "الشمس"
    },
    {
        "id": 17,
        "type": "multiple-choice",
        "prompt": "إذا وقفت مواجهاً للشمس عند الشروق، يكون اتجاه الشمال على:",
        "options": ["أمامنا", "خلفنا", "يميننا", "يسارنا"],
        "answer": "يسارنا"
    },
    {
        "id": 18,
        "type": "multiple-choice",
        "prompt": "إذا وقفت مواجهاً للشمس عند الشروق، يكون اتجاه الجنوب على:",
        "options": ["أمامنا", "خلفنا", "يميننا", "يسارنا"],
        "answer": "يميننا"
    },
    {
        "id": 19,
        "type": "multiple-choice",
        "prompt": "استعان المصريون القدماء بالنجم القطبي الشمالي لتحديد الاتجاهات في وقت:",
        "options": ["النهار", "الظهر", "الليل", "العصر"],
        "answer": "الليل"
    },
    {
        "id": 20,
        "type": "multiple-choice",
        "prompt": "استخدام المصريين القدماء للنجوم لتحديد الاتجاهات يدل على براعتهم في علم:",
        "options": ["الهندسة", "الطب", "الفلك", "الحساب"],
        "answer": "الفلك"
    },
    {
        "id": 21,
        "type": "multiple-choice",
        "prompt": "النجم القطبي الشمالي هو نجم لامع في السماء يشير دائماً إلى اتجاه:",
        "options": ["الشرق", "الغرب", "الجنوب", "الشمال"],
        "answer": "الشمال"
    },
    {
        "id": 22,
        "type": "multiple-choice",
        "prompt": "أداة تحتوي على إبرة مغناطيسية تشير دائماً لاتجاه الشمال المغناطيسي هي:",
        "options": ["الساعة", "البوصلة", "المسطرة", "الترمومتر"],
        "answer": "البوصلة"
    },
    {
        "id": 23,
        "type": "multiple-choice",
        "prompt": "الأداة الموجودة في الهواتف الذكية وتستخدم لتحديد الاتجاهات بسرعة ودقة أكبر هي:",
        "options": ["البوصلة الرقمية", "البوصلة التقليدية", "مخطط المنزل", "سارية العلم"],
        "answer": "البوصلة الرقمية"
    },
    {
        "id": 24,
        "type": "multiple-choice",
        "prompt": "عند اختيار الطريق للوصول إلى مكان ما، من المهم أن نفكر في الهدف و:",
        "options": ["السرعة فقط", "السهولة معاً", "المنحنيات فقط", "الإصلاحات"],
        "answer": "السهولة معاً"
    },
    {
        "id": 25,
        "type": "multiple-choice",
        "prompt": "الطريق المباشر الذي يبلغ طوله 500 متر ويحتوي على معلم واحد يختاره من يفضل:",
        "options": ["التسوق", "ممارسة رياضة المشي", "الوصول بسرعة", "رؤية الإصلاحات"],
        "answer": "الوصول بسرعة"
    },
    {
        "id": 26,
        "type": "true-false",
        "prompt": "تُعد الشمس إحدى الطرق الطبيعية التي تمكننا من تحديد الاتجاهات الأصلية.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 27,
        "type": "true-false",
        "prompt": "تشرق الشمس دائماً من جهة الغرب.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 28,
        "type": "true-false",
        "prompt": "يُعد اتجاه الشمال الشرقي أحد الاتجاهات الأصلية الأربعة.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 29,
        "type": "true-false",
        "prompt": "النجم القطبي الشمالي يشير دائماً إلى اتجاه الجنوب.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 30,
        "type": "true-false",
        "prompt": "تستخدم البوصلة الرقمية في الهواتف الذكية لتحديد الاتجاهات بسرعة ودقة أكبر.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 31,
        "type": "true-false",
        "prompt": "استخدم المصريون القدماء الشمس لتحديد الاتجاهات أثناء الليل.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 32,
        "type": "true-false",
        "prompt": "برع المصريون القدماء في علم الفلك واستخدموا النجوم لمعرفة الاتجاهات ليلاً.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 33,
        "type": "true-false",
        "prompt": "يقتصر اختيار الطريق للوصول إلى الأماكن على عامل السرعة فقط.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 34,
        "type": "true-false",
        "prompt": "يوجد بين كل اتجاهين أصليين اتجاه فرعي واحد.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 35,
        "type": "true-false",
        "prompt": "يُعد اتجاه الشرق أحد الاتجاهات الأصلية.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 36,
        "type": "true-false",
        "prompt": "يقع اتجاه الجنوب الغربي بين اتجاهي الشمال والغرب.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 37,
        "type": "true-false",
        "prompt": "يشير النجم القطبي في السماء دائماً إلى اتجاه الشمال.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 38,
        "type": "true-false",
        "prompt": "المكان الذي يقضي فيه التلاميذ أوقاتاً سعيدة مع المعلمين والأصدقاء هو النادي.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 39,
        "type": "true-false",
        "prompt": "الجهة المقابلة لاتجاه الشمال هي جهة الغرب.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 40,
        "type": "true-false",
        "prompt": "من الجهات الأصلية اتجاه الجنوب الغربي.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 41,
        "type": "true-false",
        "prompt": "يُعد اتجاه الشمال الغربي اتجاهاً فرعياً يقع بين الشمال والغرب.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 42,
        "type": "true-false",
        "prompt": "البوصلة هي أداة تحتوي على إبرة مغناطيسية وتستخدم حديثاً لتحديد الاتجاهات.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 43,
        "type": "true-false",
        "prompt": "يتم تقسيم المبنى من الداخل وكتابة اسم كل مكان عند رسم المخطط من قبل المهندس.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 44,
        "type": "true-false",
"prompt": "إذا واجهت الشمس عند شروقها، فإن اتجاه الشرق يكون خلفك مباشرة.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 45,
"type": "true-false",
"prompt": "يجب أن نحافظ على مدرستنا تماماً كما نحافظ على بيتنا.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 46,
"type": "true-false",
"prompt": "رسم مخطط مصغر للمكان يساعد على معرفة تفاصيله بطريقة أوضح.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 47,
"type": "true-false",
"prompt": "عند رسم المخطط، توضع النوافذ والأبواب لتسمح بدخول الأثاث فقط.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 48,
"type": "true-false",
"prompt": "الطريق الذي يحتوي على منحنيات وطوله 650 متراً ومنحنياته قليلة يختاره من يحب التسوق في الطريق.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 49,
"type": "true-false",
"prompt": "الطريق الطويل الذي يبلغ 1000 متر وبه إصلاحات يختاره من يحب ممارسة رياضة المشي.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 50,
"type": "true-false",
"prompt": "توجد أربعة اتجاهات فرعية تقع بين الاتجاهات الأصلية.",
"options": ["صواب", "خطأ"],
"answer": "صواب"

    }
],
"متوسط": [
          {
          
  "id": 1,
        "type": "multiple-choice",
        "prompt": "ما النتيجة المترتبة على رسم مخطط مصغر للمكان كأننا نراه من الأعلى؟",
        "options": [
            "معرفة تفاصيل المكان بطريقة أوضح من الوصف بالكلمات",
            "تحديد سرعة الوصول إلى الأماكن المختلفة بدقة",
            "معرفة أوقات شروق الشمس وغروبها بدقة فلكية",
            "تغيير التصميم الداخلي للمبنى تلقائياً"
        ],
        "answer": "معرفة تفاصيل المكان بطريقة أوضح من الوصف بالكلمات"
    },
    {
        "id": 2,
        "type": "multiple-choice",
        "prompt": "توضع الأبواب والنوافذ في المخططات الهندسية للمباني لسببين هما السماح بدخول الهواء و:",
        "options": ["تحديد الاتجاهات الفرعية", "دخول ضوء الشمس", "منع ممارسة رياضة المشي", "تقليل مساحة الغرف"],
        "answer": "دخول ضوء الشمس"
    },
    {
        "id": 3,
        "type": "multiple-choice",
        "prompt": "أي من المعايير التالية لا يعتمد عليها اختيار الطريق فقط ؟",
        "options": ["الهدف", "السهولة", "السرعة", "عدد غرف الدراسة"],
        "answer": "السرعة"
    },
    {
        "id": 4,
        "type": "multiple-choice",
        "prompt": "ما العبارة الدالة على أهمية المحافظة على المدرسة؟",
        "options": [
            "لأنها تحتوي على ملاعب واسعة وحدائق كبيرة",
            "لأنها بيتنا الثاني ونقضي فيها أوقاتاً سعيدة مع المعلمين والأصدقاء",
            "لأن المهندس هو الذي يصمم ويبني المنازل والمبارات الجميلة",
            "لأنها تقع دائماً في جهة الشرق من الحديقة العامة"
        ],
        "answer": "لأنها بيتنا الثاني ونقضي فيها أوقاتاً سعيدة مع المعلمين والأصدقاء"
    },
    {
        "id": 5,
        "type": "multiple-choice",
        "prompt": "اذا اختار احد الاشخاص المخطط الاطول فهو يحب:",
        "options": ["الوصول بسرعة كبيرة", "التسوق في الطريق", "ممارسة رياضة المشي", "تجنب المنحنيات"],
        "answer": "ممارسة رياضة المشي"
    },
    {
        "id": 7,
        "type": "multiple-choice",
        "prompt": "اعتمد الإنسان قديماً على الطبيعة لتحديد الاتجاهات، والظواهر الطبيعية المذكورة بالملف هي:",
        "options": ["الرياح والأمطار", "الشمس والنجوم", "الجبال والبحار", "القمح والنخيل"],
        "answer": "الشمس والنجوم"
    },
    {
        "id": 8,
        "type": "multiple-choice",
        "prompt": "إذا كان اتجاه الشمال على يسارنا عند مواجهة الشمس، فهذا يعني أننا نقف مواجهين للشمس في وقت:",
        "options": ["الغروب", "الشروق", "الظهيرة", "منتصف الليل"],
        "answer": "الشروق"
    },
    {
        "id": 9,
        "type": "multiple-choice",
        "prompt": "ما الدليل التاريخي على براعة المصريين القدماء في علم الفلك؟",
        "options": [
            "بناء غرف دراسية واسعة في المدارس",
            "استعانتهم بالنجم القطبي الشمالي لتحديد الاتجاهات ليلاً",
            "استخدام البوصلة الرقمية في الهواتف الذكية",
            "تصميم مخططات للمنازل تظهر قطع الأثاث"
        ],
        "answer": "استعانتهم بالنجم القطبي الشمالي لتحديد الاتجاهات ليلاً"
    },
    {
        "id": 10,
        "type": "multiple-choice",
        "prompt": "لماذا يسهل النجم القطبي الشمالي على الإنسان تحديد باقي الاتجاهات ليلاً؟",
        "options": [
            "لأنه يتحرك باستمرار بين الشرق والغرب",
            "لأنه يظهر في النهار والليل معاً",
            "لأنه يشير دائماً إلى اتجاه الشمال بثبات",
            "لأنه يغير لونه حسب الفصول الأربعة"
        ],
        "answer": "لأنه يشير دائماً إلى اتجاه الشمال بثبات"
    },
    {
        "id": 11,
        "type": "multiple-choice",
        "prompt": "تتميز البوصلة الرقمية عن البوصلة المغناطيسية التقليدية بأنها تحدد الاتجاهات بـ:",
        "options": [
            "الاعتماد على النجوم فقط ليلاً",
            "سرعة ودقة أكبر وعن طريق الهواتف الذكية",
            "مراعاة رسم الشمس خارج المنزل",
            "تقليل طول الطريق والمسافة"
        ],
        "answer": "سرعة ودقة أكبر وعن طريق الهواتف الذكية"
    },
    {
        "id": 17,
        "type": "multiple-choice",
        "prompt": "الجهة الفرعية التي تقع تماماً بين اتجاه الجنوب واتجاه الشرق هي:",
        "options": ["الشمال الشرقي", "الجنوب الغربي", "الجنوب الشرقي", "الشمال الغربي"],
        "answer": "الجنوب الشرقي"
    },
    {
        "id": 18,
        "type": "multiple-choice",
        "prompt": "ما الذي تشير إليه الإبرة المغناطيسية في البوصلة التقليدية دائماً؟",
        "options": ["اتجاه الشرق الجغرافي", "اتجاه الشمال المغناطيسي", "اتجاه الجنوب الفرعي", "موقع النجم القطبي ليلاً"],
        "answer": "اتجاه الشمال المغناطيسي"
    },
    {
        "id": 20,
        "type": "multiple-choice",
        "prompt": "الاتجاه الفرعي الذي يقابل تماماً اتجاه 'الجنوب الشرقي' هو اتجاه:",
        "options": ["الشمال الشرقي", "الشمال الغربي", "الجنوب الغربي", "الشمال"],
        "answer": "الشمال الغربي"
    },
    {
        "id": 21,
        "type": "multiple-choice",
        "prompt": "عند وقوفك خلف الغرب مباشرة، فإن الجهة التي تكون في مواجهتك هي جهة:",
        "options": ["الشمال", "الجنوب", "الشرق", "الغرب"],
        "answer": "الشرق"
    },
    {
        "id": 25,
        "type": "multiple-choice",
        "prompt": "الاتجاه الفرعي 'شمال غرب' يقع بين أي من الاتجاهات الأصلية؟",
        "options": ["الشمال والشرق", "الجنوب والغرب", "الشمال والغرب", "الجنوب والشرق"],
        "answer": "الشمال والغرب"
    },
    {
        "id": 26,
        "type": "true-false",
        "prompt": "يعتمد اختيار الطريق المناسب للوصول للأماكن على التفكير في الهدف والسهولة معاً وليس السرعة فقط.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 27,
        "type": "true-false",
        "prompt": "عند وقوفنا مواجهين للشمس وقت الشروق، يكون اتجاه الغرب خلفنا مباشرة.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 28,
        "type": "true-false",
        "prompt": "استخدم المصريون القدماء النجم القطبي الشمالي لتحديد الاتجاهات ومواقعهم خلال ساعات النهار.",
        "options": ["صواب", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 30,
        "type": "true-false",
        "prompt": "كل اتجاه من الاتجاهات الفرعية الأربعة يوجد دائماً بين اتجاهين أصليين.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 31,
        "type": "true-false",
        "prompt": "البوصلة الرقمية هي الأداة الحديثة التي تتيح للإنسان تحديد الاتجاهات بدقة وسرعة عبر الهواتف الذكية.",
        "options": ["صواب", "خطأ"],
        "answer": "صواب"
    },
    {
        "id": 32,
        "type": "true-false",
        "prompt": "الوصف بالكلمات يعطي تفاصيل أوضح للمكان مقارنة برسم مخطط مصغر له من الأعلى.",
        "options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 33,
"type": "true-false",
"prompt": "من القواعد الهندسية عند رسم مخطط المنزل أن يتم رسم الشمس في الفناء الداخلي للمنزل.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 36,
"type": "true-false",
"prompt": "يدل استخدام المصريين القدماء للنجم القطبي الشمالي في الليل على براعتهم الكبيرة في علم الهندسة.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 37,
"type": "true-false",
"prompt": "الاتجاه الفرعي الذي يقع بين الجنوب والغرب يسمى اتجاه الجنوب الغربي.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 39,
"type": "true-false",
"prompt": "يُعد اتجاه 'الجنوب الغربي' جهة مقابلة تماماً لاتجاه 'الشمال الشرقي'.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 40,
"type": "true-false",
"prompt": "تتميز الإبرة المغناطيسية في البوصلة التقليدية بأنها تشير دائماً لاتجاه الجنوب المغناطيسي.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 41,
"type": "true-false",
"prompt": "الجهة المقابلة لاتجاه الشمال الغربي هي جهة الجنوب الشرقي.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 42,
"type": "true-false",
"prompt": " الشخص الذي يفضل الوصول بسرعة يختار الطريق الذي به منحنيات و أطول.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 44,
"type": "true-false",
"prompt": " اذا كانت المدرسة تقع في الشمال ونظرت لها ووجدت الحديقة يمينك فإن الحديقة تقع في جهة الشرق.",
"options": ["صواب", "خطأ"],
"answer": "صواب"

},
{
"id": 46,
"type": "true-false",
"prompt": "أحد شروط رسم مخطط المبنى الصحيح هو إضافة الأبواب والنوافذ لتسمح بدخول ضوء الشمس والهواء.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 47,
"type": "true-false",
"prompt": "الاتجاه الفرعي 'الشمال الشرقي' يقع بين اتجاه الشرق واتجاه الجنوب.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 48,
"type": "true-false",
"prompt": "النجم القطبي الشمالي هو نجم لامع يستدل منه على اتجاه الشمال بثبات تامة.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 49,
"type": "true-false",
"prompt": "تعتبر 'البوصلة' و'البوصلة الرقمية' من الأدوات المخصصة لتحديد الاتجاهات.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 50,
"type": "true-false",
"prompt": "إذا كنت في الحديقة في الشمال وتريد الذهاب إلى السوق الذي في عكس اتجاه الحديقة فعليك التوجه نحو الغرب.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"

}
],
 "محترف": [
        { 
        "id": 1,
        "type": "multiple-choice",
        "prompt": "ما الفلسفة التصميمية المستنتجة من اشتراط المهندس وضع النوافذ والأبواب في المخطط الهيكلي للمبنى؟",
        "options": [
            "تحقيق الكفاءة البيئية عبر استغلال الموارد الطبيعية كالهواء وضوء الشمس",
            "تسهيل عملية توزيع قطع الأثاث الداخلي داخل الغرف",
            "إبراز المظهر الجمالي الخارجي للمبنى السكني فقط",
            "المساعدة في تحديد موقع سارية العلم بدقة"
        ],
        "answer": "تحقيق الكفاءة البيئية عبر استغلال الموارد الطبيعية كالهواء وضوء الشمس"
    },
    {
        "id": 2,
        "type": "multiple-choice",
        "prompt": "إذا قمت بوضعية محاكاة ووقفت مواجهاً للشمس في لحظة الشروق، فما هي العلاقة الهندسية الصحيحة للاتجاهات من حولك؟",
        "options": [
            "الشرق أمامك، الغرب خلفك، الشمال عن يسارك، والجنوب عن يمينك",
            "الشرق أمامك، الغرب خلفك، الشمال عن يمينك، والجنوب عن يسارك",
            "الغرب أمامك، الشرق خلفك، الشمال عن يسارك، والجنوب عن يمينك",
            "الجنوب أمامك، الشمال خلفك، الشرق عن يمينك، والغرب عن يسارك"
        ],
        "answer": "الشرق أمامك، الغرب خلفك، الشمال عن يسارك، والجنوب عن يمينك"
    },
    {
        "id": 3,
        "type": "multiple-choice",
        "prompt": "تُظهر مقارنة مخططات السير إلى الحديقة أن اختيار المسار لا يرتبط بالسرعة تجريدياً، بل بـ:",
        "options": [
            "الموازنة العقلانية بين معيار الهدف المنشود وسهولة الحركة معاً",
            "تقليل عدد المعالم الجغرافية إلى معلم واحد فقط في كل طريق",
            "تجنب الطرق التي تحتوي على منحنيات هندسية تماماً",
            "اعتماد المسارات الطويلة التي تبلغ 1000 متر بشكل دائم"
        ],
        "answer": "الموازنة العقلانية بين معيار الهدف المنشود وسهولة الحركة معاً"
    },
    {
        "id": 4,
        "type": "multiple-choice",
        "prompt": "أي من المقارنات التالية تعبر بدقة عن الفارق بين البوصلة التقليدية والبوصلة الرقمية ؟",
        "options": [
            "التقليدية تعتمد على إبرة مغناطيسية للشمال، بينما الرقمية مدمجة بالهواتف لسرعة ودقة أكبر",
            "التقليدية تستخدم نهاراً فقط، بينما الرقمية تعتمد على النجم القطبي ليلاً",
            "التقليدية مخصصة لرسم المخططات الهندسية، بينما الرقمية مخصصة لحساب مساحات الغرف",
            "التقليدية تحدد الاتجاهات الأصلية، بينما الرقمية تقتصر على الاتجاهات الفرعية"
        ],
        "answer": "التقليدية تعتمد على إبرة مغناطيسية للشمال، بينما الرقمية مدمجة بالهواتف لسرعة ودقة أكبر"
    },
    {
        "id": 5,
        "type": "multiple-choice",
        "prompt": "الاعتماد الصارم للمصريين القدماء على النجم القطبي الشمالي لتحديد الاتجاهات ليلاً يعد تطبيقاً لـ:",
        "options": [
            "علم الفلك القائم لبعض الأجرام السماوية",
            "علم الهندسة المعمارية الخاص بتصميم المدارس والمنازل",
            "تطوير أدوات الملاحة الرقمية الحديثة في الهواتف الذكية",
            "تحديد المسارات القصيرة والمباشرة أثناء رحلات السير نهاراً"
        ],
        "answer": "علم الفلك القائم لبعض الأجرام السماوية"
    },
    {
        "id": 6,
        "type": "multiple-choice",
        "prompt": "إذا تحركت في مسار عكسي تماماً لاتجاه 'الجنوب الغربي'، فما هو الاتجاه الدقيق الذي تسير نحوه؟",
        "options": ["الشمال الغربي", "الجنوب الشرقي", "الشمال الشرقي", "الشرق الجغرافي"],
        "answer": "الشمال الشرقي"
    },
    {
        "id": 7,
        "type": "multiple-choice",
        "prompt": "عند تحليل جدول مقارنة الطرق، ما هو التفسير المنطقي لاختيار شخص ما للمخطط الثالث (طوله 1000 متر وبه إصلاحات)؟",
        "options": [
            "رغبته المسبقة في ممارسة رياضة المشي كهدف أساسي للرحلة",
            "تفضيله للوصول إلى الحديقة بأسرع وقت ممكن وبأقل مجهود",
            "حاجته الماسة للتسوق وشراء المستلزمات من البقالة في الطريق",
            "اعتماده على البوصلة المغناطيسية لتفادي المنحنيات"
        ],
        "answer": "رغبته المسبقة في ممارسة رياضة المشي كهدف أساسي للرحلة"
    },
    {
        "id": 9,
        "type": "multiple-choice",
        "prompt": "إذا كنت تقف عكس الشرق وتريد الانتقال إلى الامام ، فانك أن تتجه مباشرة نحو:",
        "options": ["الشرق", "الغرب", "الشمال الغربي", "الجنوب الغربي"],
        "answer": "الغرب"
    },
    {
        "id": 11,
        "type": "multiple-choice",
        "prompt": "الاتجاه الفرعي الذي يقع هندسياً بين الاتجاه الأصلي الغربي والاتجاه الأصلي الشمالي هو اتجاه:",
        "options": ["الشمال الشرقي", "الجنوب الغربي", "الجنوب الشرقي", "الشمال الغربي"],
        "answer": "الشمال الغربي"
    },
    {
        "id": 12,
        "type": "multiple-choice",
        "prompt": "المسار الذي يتسم بأنه 'مباشر' ويحتوي على 'معلم واحد' فقط يقدم أفضل كفاءة في:",
        "options": ["توفير فرص التسوق", "سرعة الوصول للمكان", "ممارسة الرياضة البدنية", "رؤية أعمال الإصلاحات"],
        "answer": "سرعة الوصول للمكان"
    },
    {
        "id": 13,
        "type": "multiple-choice",
        "prompt": "الجهة المقابلة والمضادة تماماً لاتجاه 'الشمال الغربي' في بوصلة الاتجاهات هي جهة:",
        "options": ["الشمال الشرقي", "الجنوب الشرقي", "الجنوب الغربي", "الجنوب"],
        "answer": "الجنوب الشرقي"
    },
    {
        "id": 14,
        "type": "multiple-choice",
        "prompt": "ما الخصائص الفلكية المحددة لأهمية النجم القطبي الشمالي التي جعلته أداة ملاحية تاريخية؟",
        "options": [
            "ثبات مؤشره الاتجاهي نحو الشمال وكونه نجماً لامعاً يستدل به ليلاً",
            "ظهوره المتكرر نهاراً مع حركة الشمس من الشرق إلى الغرب",
            "قدرته على تحديد المواقع بدقة موازية للبستنة الرقمية للهواتف",
            "تغير موقعه الجغرافي بانتظام بين الفصول الأربعة"
        ],
        "answer": "ثبات مؤشره الاتجاهي نحو الشمال وكونه نجماً لامعاً يستدل به ليلاً"
    },
    {
        "id": 16,
        "type": "multiple-choice",
        "prompt": "عند وقوف شخص ما بحيث يكون اتجاه الجنوب على يمينه مباشرة، فهذا يعني منطقياً أنه يواجه جهة:",
        "options": ["الغرب", "الشمال", "الشرق", "الجنوب الغربي"],
        "answer": "الشرق"
    },
    {
        "id": 17,
        "type": "multiple-choice",
        "prompt": "كم عدد الاتجاهات الفرعية الكلية المحصورة بين المحاور الأصلية الأربعة؟",
        "options": ["اتجاهان", "ثلاثة اتجاهات", "أربعة اتجاهات", "ثمانية اتجاهات"],
        "answer": "أربعة اتجاهات"
    },
    {
        "id": 19,
        "type": "multiple-choice",
        "prompt": "تحديد العلاقة المكانية بأن 'المستشفى يقع جنوب شرق الحديقة' يعني أنه للعودة من المستشفى للحديقة يجب التوجه نحو:",
        "options": ["الشمال الشرقي", "الجنوب الغربي", "الشمال الغربي", "الجنوب الشرقي"],
        "answer": "الشمال الغربي"
    },
    {
        "id": 21,
        "type": "multiple-choice",
        "prompt": "تعتمد آلية عمل البوصلة التقليدية في تحديد الاتجاهات الجغرافية على الخصائص السيادية لـ:",
        "options": ["الإبرة المغناطيسية", "الشمس خارج المنزل", "الهواتف الذكية", "الرسومات الهندسية"],
        "answer": "الإبرة المغناطيسية"
},
{
"id": 24,
"type": "multiple-choice",
"prompt": "إذا قيل أن 'المنزل يقع شمال الحديقة'، فما هو موقع الحديقة الإحداثي بالنسبة للمنزِل؟",
"options": ["شرق المنزل", "غرب المنزل", "شمال المنزل", "جنوب المنزل"],
"answer": "جنوب المنزل"
},
{
"id": 25,
"type": "multiple-choice",
"prompt": "أحد المبادئ الإلزامية التي يطبقها الطلاب عند رسم مخططاتهم المستقبلية لضمان صحة التصميم هندسياً وفلكياً هو:",
"options": [
"رسم الشمس في الفضاء الخارجي خارج حدود المنزل",
"وضع ست غرف دراسية كاملة وملاعب واسعة",
"تلوين الشرفة باللون الأحمر وغرفة الاستقبال بالأزرق",
"إلغاء وضع الأبواب والنوافذ لتوفير مساحة إضافية"
],
"answer": "رسم الشمس في الفضاء الخارجي خارج حدود المنزل"
},
{
"id": 26,
"type": "true-false",
"prompt": "الهدف الرئيسي من رسم المخططات المعمارية للمباني من الأعلى هو تلافي عجز الوصف في نقل تفاصيل المكان بدقة.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 27,
"type": "true-false",
"prompt": "تتحرك الشمس ظاهرياً وتشرق يومياً من جهة الغرب الجغرافي وتغرب في جهة الشرق.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 28,
"type": "true-false",
"prompt": " التفكير في سرعة الوصول هو العامل الوحيد والكامل الحاكم عند مفاضلة الإنسان بين الطرق.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 29,
"type": "true-false",
"prompt": "تتطابق خطوط الاتجاهات الفرعية تماماً مع خطوط الاتجاهات الأصلية وتتداخل معها بدون أي فواصل زاوية.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 30,
"type": "true-false",
"prompt": "استخدام البوصلة الرقمية عبر الهواتف الذكية يمنح المستخدم تفوقاً ملاحياً من حيث السرعة والدقة الفائقة في رصد الاتجاهات.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 31,
"type": "true-false",
"prompt": "اعتمد المصريون القدماء على رصد النجم القطبي الشمالي كأداة فلكية ملاحية لتوجيه حركتهم وتحديد اتجاهاتهم خلال ساعات النهار.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 33,
"type": "true-false",
"prompt": "يُشتق اتجاه 'الشمال الشرقي' كاتجاه فرعي من خلال وقوعه الجغرافي بين المحورين الأصليين: الشمال والشرق.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 34,
"type": "true-false",
"prompt": "تتميز الإبرة المغناطيسية في أدوات البوصلة التقليدية بأنها تنجذب وتتجه بثبات دائم نحو اتجاه الجنوب المغناطيسي.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 35,
"type": "true-false",
"prompt": " المسار الذي يحتوي على منحنيات بسيطة وطوله 650 متراً يوفر سرعة وصول يوصف مستواها بأنه 'متوسط'.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 36,
"type": "true-false",
"prompt": "يعتبر اتجاه 'الجنوب الغربي' هو الجهة العكسية والمقابلة تماماً على بوصلة القياس لاتجاه 'الشمال الغربي'.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 37,
"type": "true-false",
"prompt": "الالتزام بوضع الأبواب والنوافذ داخل المخطط المعماري يستهدف توفير مسارات بيئية لدخول الهواء النقي وضوء الشمس للمبنى.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 40,
"type": "true-false",
"prompt": "الجهة المقابلة والمضادة مباشرة لاتجاه الغرب الجغرافي هي جهة الشمال الأصلي.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 41,
"type": "true-false",
"prompt": "النجم القطبي الشمالي هو جرم فلكي لامع ويتميز بثبات إشارته الاتجاهية دائماً نحو قطب الشمال.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 42,
"type": "true-false",
"prompt": "برع المصريون القدماء في علم الفلك، وكان رصدهم للنجوم ليلاً دليلاً حاسماً على هذا التفوق العلمي والتاريخي.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 43,
"type": "true-false",
"prompt": "تُصنف اتجاهات (الشمال، الجنوب، الشرق، الغرب) كاتجاهات فرعية في بيئة تحديد المواقع.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
"id": 45,
"type": "true-false",
"prompt": "عند وقوفك في وضعية مواجهة شروق الشمس، فإن اتجاه الشمال يقع جغرافياً على جهة يدك اليمنى.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"
},
{
 "id": 47,
    "type": "true-false",
    "prompt": " عند الوقوف مواجهاً للشمس وقت الشروق، يكون الغرب خلفنا مباشرة.",
    "options": ["صواب", "خطأ"],
    "answer": "صواب"
},
{
"id": 48,
"type": "true-false",
"prompt": "يقع اتجاه 'الجنوب الشرقي' كاتجاه فرعي دقيق محصور تماماً بين اتجاهي الجنوب والشرق الأصليين.",
"options": ["صواب", "خطأ"],
"answer": "صواب"
},
{
"id": 49,
"type": "true-false",
"prompt": " اختيار مسار المشي الطويل المليء بالإصلاحات هو الخيار المفضل لمن يبتغي سرعة الوصول.",
"options": ["صواب", "خطأ"],
"answer": "خطأ"

    }
  ]
}


@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB.get("متوسط", []))
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "prompt": questions[current_index]['prompt'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": (ans == questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة الدرس الاول دراسات اجتماعية رابعة ابتدائي    </div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">السؤال: <strong style="color: #114b3e;">{{ current_num }} من {{ total_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
                <p><strong>سؤال {{ current_num }}:</strong> {{ question.prompt }}</p>
               
                <div class="options-list">
                    {% for opt in question.options %}
                        <label class="option-item">
                            <input type="radio" name="current_answer" value="{{ opt }}" required> {{ opt }}
                        </label>
                    {% endfor %}
                </div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
