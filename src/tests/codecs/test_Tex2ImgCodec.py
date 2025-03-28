from PIL.Image import Image
from AEPi import CompressionFormat
from AEPi.codecs.Tex2ImgCodec import Tex2ImgCodec
from PIL import Image
import pytest

from AEPi.constants import CompressionFormat

# Paths to the smiley image PNGs, after a round trip of compression and then decompression using AEIEditor.
SMILEY_ROUNDTRIP_PNG_PATHS = {
    CompressionFormat.PVRTC14A: "src/tests/assets/roundtrip/RGB/smiley_PVRTC14A.png",
    CompressionFormat.ATC: "src/tests/assets/roundtrip/RGB/smiley_ATC.png",
}

# This is the raw pixels of the smiley image compressed using AEIEditor.
SMILEY_COMPRESSED_RAW = {
    CompressionFormat.PVRTC14A: b"\x00\x55\xFF\xFF\x1A\x80\xFF\xFF\xFF\xFF\xFF\xFF\x00\x80\xFF\xFF\x00\x55\xFF\xFF\x5C\x80\xFF\xFF\xFF\xFF\xFC\xFF\x00\x80\xFF\xFF\xFF\xFF\x3F\xFF\x00\x80\xFF\xFF\xFF\xFF\xFF\xFF\x90\xB9\xFF\xFF\xFF\xFF\xFF\x00\x60\xCC\xFF\xFF\x03\xC3\xFF\xFF\x4E\xD5\xFF\xFF\x00\x55\xFF\xFF\x1C\x88\xFF\xFF\xFF\xFF\xCF\xFF\x00\x80\xFF\xFF\x00\xD5\xFF\xFF\x5E\x9C\xFF\xFF\xFF\xFF\xFF\xFF\xFC\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x80\xFF\xFF\xFF\xFF\xFF\xFF\x8C\xA9\xFF\xFF\xFF\xFF\xF3\xFC\x00\x80\xFF\xFF\xFF\xFF\x3F\x00\xA2\xA5\xFF\xFF\x00\x55\xFF\xFF\x1A\x80\xFF\xFF\xFF\xFF\xFF\xFF\x00\x80\xFF\xFF\x00\x55\xFF\xFF\x5C\x80\xFF\xFF\xFF\xFF\xFC\xFF\x00\x80\xFF\xFF\xFF\xFF\x3F\xFF\x00\x80\xFF\xFF\xFF\xFF\xFF\xFF\x90\xB9\xFF\xFF\xFF\xFF\xFF\x00\x60\xCC\xFF\xFF\x03\xC3\xFF\xFF\x4E\xD5\xFF\xFF\x00\x55\xFF\xFF\x1C\x88\xFF\xFF\xFF\xFF\xCF\xFF\x00\x80\xFF\xFF\x00\xD5\xFF\xFF\x5E\x9C\xFF\xFF\xFF\xFF\xFF\xFF\xFC\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x80\xFF\xFF\xFF\xFF\xFF\xFF\x8C\xA9\xFF\xFF\xFF\xFF\xF3\xFC\x00\x80\xFF\xFF\xFF\xFF\x3F\x00\xA2\xA5\xFF\xFF",
    CompressionFormat.ATC: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xF7\x20\xFF\xFF\x00\x55\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xF7\x20\xFF\xFF\x00\x55\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xF7\x20\xFF\xFF\x00\x55\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xF7\x20\xFF\xFF\x00\xD5\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFC\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xCF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\x3F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xE7\xD0\xFF\xFF\xFF\xFF\xFF\xA8\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xF3\xFC\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xE7\x54\xFF\xFF\x03\xC3\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x87\x25\xFF\xFF\xFF\xFF\x3F\x00",
}

CODEC = Tex2ImgCodec()

def smileyRoundtripImage(format: CompressionFormat):
    png = Image.open(SMILEY_ROUNDTRIP_PNG_PATHS[format])

    if png.mode != format.pillowMode:
        return png.convert(format.pillowMode)
    
    return png


# Tex2ImgCodec segfaults decoding PVRTC with all tests (#29)
# @pytest.mark.codecs
# @pytest.mark.codecs_PVRTC14A
# def test_decompress_PVRTC14A_succeeds():
#     with smileyRoundtripImage(CompressionFormat.PVRTC14A) as expected:
#         compressed = SMILEY_COMPRESSED_RAW[CompressionFormat.PVRTC14A]
#         actual = CODEC.decompress(compressed, CompressionFormat.PVRTC14A, expected.width, expected.height, None)
#         for coords in zip(range(expected.width), range(expected.height)):
#             assert expected.getpixel(coords) == actual.getpixel(coords) # type: ignore[reportUnknownMemberType]

@pytest.mark.skip(reason="segfault due to tex2img dependency")
@pytest.mark.codecs
@pytest.mark.codecs_ATC
def test_decompress_ATC_succeeds():
    with smileyRoundtripImage(CompressionFormat.ATC) as expected:
        compressed = SMILEY_COMPRESSED_RAW[CompressionFormat.ATC]
        actual = CODEC.decompress(compressed, CompressionFormat.ATC, expected.width, expected.height, None) \
            .convert(expected.mode)
        for coords in zip(range(expected.width), range(expected.height)):
            assert expected.getpixel(coords) == actual.getpixel(coords) # type: ignore[reportUnknownMemberType]

@pytest.mark.skip(reason="segfault due to tex2img dependency")
@pytest.mark.codecs
@pytest.mark.codecs_DXT1
def test_decompress_DXT1_succeeds():
    with smileyRoundtripImage(CompressionFormat.DXT1) as expected:
        compressed = SMILEY_COMPRESSED_RAW[CompressionFormat.DXT1]
        actual = CODEC.decompress(compressed, CompressionFormat.DXT1, expected.width, expected.height, None) \
            .convert(expected.mode)
        for coords in zip(range(expected.width), range(expected.height)):
            assert expected.getpixel(coords) == actual.getpixel(coords) # type: ignore[reportUnknownMemberType]

@pytest.mark.skip(reason="segfault due to tex2img dependency")
@pytest.mark.codecs
@pytest.mark.codecs_DXT5
def test_decompress_DXT5_succeeds():
    with smileyRoundtripImage(CompressionFormat.DXT5) as expected:
        compressed = SMILEY_COMPRESSED_RAW[CompressionFormat.DXT5]
        actual = CODEC.decompress(compressed, CompressionFormat.DXT5, expected.width, expected.height, None) \
            .convert(expected.mode)
        for coords in zip(range(expected.width), range(expected.height)):
            assert expected.getpixel(coords) == actual.getpixel(coords) # type: ignore[reportUnknownMemberType]

@pytest.mark.skip(reason="segfault due to tex2img dependency")
@pytest.mark.codecs
@pytest.mark.codecs_ETC1
def test_decompress_ETC1_succeeds():
    with smileyRoundtripImage(CompressionFormat.ETC1) as expected:
        compressed = SMILEY_COMPRESSED_RAW[CompressionFormat.ETC1]
        actual = CODEC.decompress(compressed, CompressionFormat.ETC1, expected.width, expected.height, None) \
            .convert(expected.mode)
        for coords in zip(range(expected.width), range(expected.height)):
            assert expected.getpixel(coords) == actual.getpixel(coords) # type: ignore[reportUnknownMemberType]
