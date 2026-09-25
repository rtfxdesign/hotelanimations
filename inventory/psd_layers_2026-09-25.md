# PSD layer maps — measured 2026-09-25 (psd-tools 1.10, read-only)

All PSDs are 8-bit RGB. `bbox` is (left, top, right, bottom) in canvas pixels; `size` is the layer's own pixel extent. Every layer is visible at 100% opacity. No groups, masks or adjustment layers in any file.

## Giraffe Manor/upscaled/manor01.psd — canvas 2752×1536
| layer | bbox | size | note |
|---|---|---|---|
| background | 0,0 → 2752,1536 | 2752×1536 | = `manor01_background.png` (giraffes painted out) |
| giraffe02 | 1578,1049 → 1910,1535 | 332×486 | = `manor01_giraffe02.png`; foreground giraffe on the steps, 32 % of frame height, touches bottom edge |
| giraffe01 | 1262,869 → 1440,1159 | 178×290 | = `manor01_giraffe01.png`; giraffe by the terrace, 19 % of frame height |

## 5th ave hotel NYC/upscaled/turtlewalkers.psd — canvas 4346×2444 (16:9, 1.778)
| layer | bbox | size |
|---|---|---|
| background | 0,0 → 4346,2444 | 4346×2444 |
| man | 1754,226 → 2420,1805 | 666×1579 |
| turtle | 1934,1272 → 3397,2116 | 1463×844 |
| leash | 1798,1095 → 2380,1431 | 582×336 |
| woman | 742,196 → 1873,2000 | 1131×1804 |

The four PNG layer exports in the same folder are these layers cropped to bounds (`man.png` 666×1579, `woman.png` 1131×1804, `turtle.png` 1463×844, `leash.png` 582×336). To re-place them, use the bbox origins above. Note `turtlewalkers.png` (2896×2172, 4:3) is **not** a flatten of this PSD; it is the 2× of the original 1448×1086 plate before the canvas was widened to 16:9.

## 5th ave hotel NYC/upscaled/turtle.psd — canvas 3072×2048 (3:2)
| layer | bbox | size |
|---|---|---|
| Layer 0 | 144,363 → 2947,1661 | 2803×1298 |

= `turtle02.png` 2803×1298 (the isolated gold tortoise, 2× of the 1536×1024 original).

## 5th ave hotel NYC/upscaled/fifthave.psd — canvas 894×894
| layer | bbox | size |
|---|---|---|
| fifthavenue | 0,0 → 894,894 | 894×894 |
| fifthavenue copy | 0,0 → 894,894 | 894×894 |

2× of the 447×447 `orig/images.jpg` roundel. Small; see the logo findings in the inventory report.

## Miavana/upscaled/miavana.psd — canvas 2508×1411 (1.777 ≈ 16:9)
| layer | bbox | size | export |
|---|---|---|---|
| Layer 0 (background, sage) | 0,0 → 2508,1411 | 2508×1411 | `miavana_0005_Layer-0.png` |
| bytimeandtide | 988,1270 → 1576,1328 | 588×58 | `miavana_0004_bytimeandtide.png` |
| islandsanctuary | 439,835 → 2123,936 | 1684×101 | `miavana_0003_islandsanctuary.png` |
| miavana | 145,427 → 2405,628 | 2260×201 | `miavana_0002_miavana.png` |
| Layer 2 (left lemur, seated on the M) | 44,230 → 270,862 | 226×632 | `miavana_0000_left_lemur.png` |
| Layer 1 (right lemur, hanging from last A) | 2208,420 → 2364,1023 | 156×603 | `miavana_0001_right_lemur.png` |

`miavana copy.png` (2508×1411) is a flatten of this PSD. The lemur layers are 632 px and 603 px tall on a 1411 px canvas: at HD (1080 px) they land at roughly 480 px and 460 px tall. They are the small, soft lemurs from the original 1254 px lock-up, not the 2.7–3.2 k cut-outs (`lemur.png`, `lemur2.png`, `lemur3.png`).
