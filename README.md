# Unlock845

**This project aims to unlock your phone bootloader with only one script. Use it at your own risk!**

**Supported phones:** 

[Click here](https://github.com/log1cs/Unlock845/blob/main/SupportedDevices.md)

# How this script works?

Basically it will flash a Prototype ABL taken from an LGE SDM845 phone and will trigger your phone to Fastboot Mode. After that it will flash the FRP Image that has been patched (patched to get OEM Unlock enabled) and will unlock your bootloader in under ~2 minutes then it will reflash all of your phone partition to get you into Download Mode. After that it will ask for your KDZ (firmware file) to flash in Download Mode in order to prevent Fastboot Mode loop.

**Attention: If you are Windows 7/8.1 users then use the W7_W8.1 version**


**Head to Releases if you want to download this script**

You can extract it everywhere you wanted to. (Huge thanks to [vvanloc](https://github.com/vvanloc) for making this) 

**Preparation**

- Your phone's KDZ (My suggestion: better use a KDZ that ends with 30x in the file name. x here stands for firmware level, and it could be a,b,c,d,e,f,g,h. There might be a newer firmware in the future, but it doesn't matter anyways.)
- Windows PC
- A cable with data transfer

**USAGE:**

1 - Reboot your phone into EDL mode.

2 - Let the tool does the rest, also don't forget to follow the tool's steps. (Credit to [vvanloc](https://github.com/vvanloc) for making the tool automatically detect the COM port, huge thanks)

3 - Drag and drop your KDZ when the tool asked.

4 - Done! Your bootloader will be unlocked.

**Related**

How to enter EDL Mode on the V30/G7/V40/V50/G8/G8X:

![ezgif-1-7f9379ed0b3d](https://user-images.githubusercontent.com/60842977/132087777-a1b574f9-399b-485f-874b-0c536166055b.gif)

1 - Connect your USB cable. Then hold your Power Button and your Volume Down button till you see the screen goes black.

2 - As soon as the screen goes black, still hold Power and Vol - , press Vol + repeatedly.

3 - Go to Device Manager, it will show you QHSUSB_BULK or Qualcomm HS-USB QLoader 9008(COMx)


**FAQ:**

**My phone showing Press any key to shut down, what should i do?**

Use the FastbootFix included in the folder then reboot your phone in bootloader mode again. 
Run FastbootFix as administrator and it will work.

**Vietnamese:**

# Unlock845

**Dự án này giúp bạn mở khoá bootloader chỉ với 1 tệp lệnh. Hãy sử dụng nó cẩn thận!**

**Thiết bị được hỗ trợ:** 

[Bấm vào đây](https://github.com/log1cs/Unlock845/blob/main/SupportedDevices.md)

# Script được chạy như thế nào?

Bản chất script sẽ nạp Prototype ABL (được lấy từ 1 máy mẫu dùng chip SDM845 của LGE) trong chế độ EDL. Khi nạp xong thì script sẽ nạp phân vùng FRP đã được patch để mở OEM Unlock và máy sẽ được unlock không dưới 2 phút. Khi unlock xong thì script sẽ nạp tất cả các phân vùng gốc trong máy lại và nhảy vào Download Mode.
Trong Download Mode thì script sẽ hỏi người dùng KDZ (file firmware của máy) và nạp để tránh hiện tượng treo ở Fastboot Mode.

**Chú ý: Nếu bạn là người dùng Windows 7 và Windows 8.1 thì hãy nhớ sử dụng phiên bản có dòng W7_8.1.**



**Tải phần mềm ở phần Releases.**

Bạn có thể giải nén ở đâu cũng được. (Cảm ơn [vvanloc](https://github.com/vvanloc) vì phần tự đổng scan cổng USB) 

 **Chuẩn bị**

- 1 file KDZ (tốt nhất nên tìm các bản KDZ có đuôi từ 30 (a->h) để được đảm bảo sự an toàn cao nhất)
- Windows PC
- Một cọng cáp có khả năng truyền dữ liệu

**Cách sử dụng**

1 - Khởi động điện thoại của bạn vào EDL Mode.

2 - Để tool làm nốt phần còn lại. Và hãy làm theo chỉ dẫn của tool.

3 - Kéo thả KDZ vào khi được hỏi và bấm Enter.

4 - Xong! Bootloader sẽ được unlock.

**Cách kết nối điện thoại vào EDL**

![ezgif-1-7f9379ed0b3d](https://user-images.githubusercontent.com/60842977/132087777-a1b574f9-399b-485f-874b-0c536166055b.gif)

1 - Kết nối cáp từ điện thoại vào máy tính. Sau đó giữ nguồn và giảm âm lượng cho đến khi màn hình đen.

2 - Khi màn hình tắt đi, vẫn giữ Nguồn và giảm âm lượng, hãy bấm tăng âm lượng liên tục.

3 - Vào Device Manager, bạn sẽ thấy QHSUSB_BULK hoặc Qualcomm HS-USB QLoader 9008(COMx)


**Câu hỏi thường gặp:**

**Trên điện thoại hiện "Press any key to shut down", tôi phải làm thế nào?**

Dùng FastbootFix đặt trong thư mục gốc của phần mềm, khởi động lại máy vào bootloader.

Lưu ý: Nhớ chạy FastbootFix dưới quyền administrator
