# Pegasus Three - OSINT Toolkit

A comprehensive Open Source Intelligence (OSINT) framework for information gathering, profiling, and reconnaissance from publicly available sources.

## ⚠️ Legal Disclaimer

This tool is designed for **LEGAL AND ETHICAL USE ONLY**. Users must comply with all applicable laws and regulations. This includes:

- Obtaining proper authorization before conducting investigations
- Respecting privacy laws and regulations (GDPR, CCPA, etc.)
- Using gathered information responsibly and ethically
- NOT using this tool for harassment, stalking, or malicious purposes

**The developers assume no liability for misuse of this software.**

## Features

### 🔍 Core Modules

1. **OSINT Module** - Open source intelligence gathering
   - Domain/IP reconnaissance
   - WHOIS lookups
   - DNS enumeration
   - Subdomain discovery
   
2. **Social Media Intelligence** - Public profile analysis
   - Username search across platforms
   - Profile information gathering
   - Public post analysis
   
3. **Network Intelligence** - Network reconnaissance
   - Port scanning
   - Service detection
   - Network mapping
   
4. **Metadata Extraction** - File analysis
   - EXIF data extraction
   - Document metadata
   - Geolocation from images
   
5. **Email Intelligence** - Email investigation
   - Email validation
   - Breach database checks
   - Email format patterns
   
6. **Phone Intelligence** - Phone number analysis
   - Carrier lookup
   - Location information
   - Number validation
   
7. **Data Profiling** - Information aggregation
   - Profile building from multiple sources
   - Timeline creation
   - Relationship mapping
   
8. **Report Generation** - Documentation
   - HTML reports
   - PDF exports
   - JSON data dumps

## Installation

```bash
# Clone the repository
git clone https://github.com/sobri3195/pegasus-three.git
cd pegasus-three

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py install
```

## Quick Start

```bash
# Basic OSINT scan
python pegasus.py --target example.com --module osint

# Social media username search
python pegasus.py --username johndoe --module social

# Phone number lookup
python pegasus.py --phone +1234567890 --module phone

# Email investigation
python pegasus.py --email target@example.com --module email

# Full profile generation
python pegasus.py --target "John Doe" --profile --output report.html
```

## Usage Examples

### Domain Investigation
```bash
python pegasus.py --domain example.com --deep-scan
```

### Multi-source Profiling
```bash
python pegasus.py --target "John Doe" --username johndoe --email john@example.com --profile
```

### Network Reconnaissance
```bash
python pegasus.py --ip 192.168.1.1 --scan-ports --service-detection
```

## Configuration

Edit `config.json` to customize:
- API keys for various services
- Scan intensity levels
- Output formats
- Proxy settings

## Requirements

- Python 3.8+
- Internet connection
- API keys for enhanced features (optional)

## Ethical Guidelines

1. **Authorization**: Always obtain proper authorization before investigating
2. **Privacy**: Respect individuals' privacy rights
3. **Legality**: Ensure compliance with local laws
4. **Responsibility**: Use information gathered responsibly
5. **Transparency**: Be transparent about your intentions when possible

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file for details

## Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

### Contact

- 📧 Email: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- 🐙 GitHub: [github.com/sobri3195](https://github.com/sobri3195)
- 💰 Donasi: [https://lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)

### Social Media & Community

- 🎥 YouTube: [Muhammad Sobri Maulana](https://www.youtube.com/@muhammadsobrimaulana6013)
- 📱 TikTok: [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- 💬 Telegram: [winlin_exploit](https://t.me/winlin_exploit)
- 👥 WhatsApp Group: [Join Here](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

## 100 Fitur Baru

Berikut adalah 100 peningkatan/fitur baru yang menambah kapabilitas Pegasus Three tanpa mengubah prinsip legal & etis pemakaian:

1. Peningkatan parser WHOIS dengan ekstraksi kontak penyalahgunaan registrar
2. Lookup ASN untuk IP terkait
3. Deteksi status DNSSEC
4. Dukungan reverse WHOIS berbasis email/domain (metadata saja)
5. Deteksi protokol HTTP/2 dan HTTP/3
6. Deteksi CDN dan identifikasi providernya
7. Heuristik deteksi WAF
8. Pengambilan dan parsing robots.txt serta security.txt
9. Penemuan dan ringkasan parsing sitemap.xml
10. Enumerasi protokol TLS dan cipher suite
11. Pemeriksaan HSTS dan status preload
12. Heuristik deteksi open redirect (aman)
13. Analisis record SPF, DKIM, dan DMARC
14. Inspeksi kebijakan CORS
15. Ringkasan analisis Content-Security-Policy
16. Fingerprinting tumpukan teknologi dari header dan HTML
17. Inventarisasi URL berbasis sitemap
18. Pencocokan hash favicon (siap hash Shodan)
19. Probing jalur panel admin umum (non-invasif)
20. Utilitas kanonikal dan normalisasi URL
21. Ekstraksi URL avatar/gambar untuk profil sosial
22. Pembangunan graph tautan profil lintas platform
23. Pengambilan jumlah follower/following publik (jika tersedia)
24. Penandaan kata kunci bio untuk klasifikasi cepat
25. Saran kemiripan username dan variannya
26. Deteksi platform sekali-pakai/throwaway
27. Pengambilan sadar rate-limit dengan backoff untuk jejaring sosial
28. Estimasi tanggal pembuatan akun berbasis heuristik
29. Pembuatan placeholder tautan screenshot profil
30. Modularisasi ruleset platform sosial untuk pembaruan mudah
31. Cek keterjangkauan ICMP dengan statistik packet loss
32. Enrichment geolokasi pada hop traceroute
33. Pengecekan layanan UDP umum (probe aman)
34. Skoring entropi banner untuk mendeteksi honeypot
35. Penangkapan sertifikat TLS layanan pada port dikenal
36. Sapu reverse DNS untuk subnet
37. Pemahaman rentang RFC1918 dan bogon
38. Enumerasi dasar SMB/NetBIOS (non-intrusif)
39. Penangkapan fingerprint kunci host SSH
40. Pemeriksaan string komunitas SNMP dasar (public saja, aman)
41. Deteksi catch-all pada domain email
42. Simulasi probe SMTP VRFY/RCPT (aman, tanpa mengirim)
43. Ringkasan jumlah pelanggaran (breach) per sumber
44. Generasi hash Gravatar dari email
45. Deteksi akun-peran umum (admin@, info@, dll.)
46. Perluasan katalog penyedia email sekali-pakai
47. Pembaruan blacklist domain surat sementara
48. Saran pengetikan salah (typo-squatting) email
49. Analisis prioritas MX dan identifikasi penyedia
50. Grading penegakan kebijakan DMARC
51. Peningkatan pemformatan nomor per wilayah
52. Pemurnian heuristik risiko nomor
53. Petunjuk deteksi nomor yang dipindahkan (ported)
54. Petunjuk penyedia nomor virtual/throwaway
55. Saran jendela komunikasi sadar zona waktu
56. Integrasi placeholder lookup CNAM
57. Analisis national destination code
58. Kategori keterjangkauan nomor (likely/unknown)
59. Deteksi duplikasi nomor di seluruh dataset
60. Pemetaan risiko negara untuk nomor telepon
61. Tautan peta dari EXIF GPS dengan estimasi akurasi
62. Referensi kerentanan berdasarkan merek/model kamera
63. Ekstraksi thumbnail bila tersedia
64. Deteksi file tertanam pada PDF
65. Parsing revisi dokumen dan produser
66. Multi-hash: MD5/SHA1/SHA256
67. Deteksi MIME type dari magic bytes
68. Perhitungan ukuran berkas dan entropi
69. Ringkasan histogram warna untuk gambar
70. Deteksi orientasi dan rotasi gambar
71. Resolver entitas untuk melebur duplikat lintas sumber
72. Penyusunan timeline dengan skor kepercayaan per peristiwa
73. Ekspor matriks relasi dalam JSON
74. Heuristik penemuan alias dan AKA
75. Ekstraksi afiliasi organisasi
76. Klasterisasi lokasi dari beragam sumber
77. Penandaan faktor risiko berbasis pola
78. Rincian penjelasan skor kepercayaan
79. Pembobotan reliabilitas sumber
80. Mode redaksi profil untuk berbagi aman
81. Tema gelap untuk laporan HTML
82. Kontrol sertakan/abaikan per bagian laporan
83. Peningkatan auto-generasi ringkasan eksekutif
84. Daftar lampiran bukti di laporan
85. Tautan peta inline untuk temuan geo
86. Paginasi PDF dan daftar isi
87. Versi skema JSON untuk ekspor
88. Mode minimal untuk laporan TXT
89. Preset --deep-scan per modul
90. Flag --rate-limit dan --concurrency
91. Opsi --proxy dan kompatibel Tor membaca dari config
92. Kontrol --retries dan backoff eksponensial
93. Penanganan --output-dir terpadu dengan nama berkas otomatis
94. Indikator progres dan spinner yang informatif
95. Output konsol berwarna berdasarkan tingkat keparahan
96. Redaksi PII di log sebagai default
97. Default yang lebih aman untuk timeout dan retries
98. Opt-in untuk pemeriksaan berpotensi intrusif
99. ID jejak audit (audit trail) antar-run
100. Peningkatan disclaimer legal/etik yang ditampilkan di CLI

## Support

For issues and questions, please open a GitHub issue or contact via email.
