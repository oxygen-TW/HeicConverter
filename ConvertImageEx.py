class ConvertImageFileNotFound(Exception):
    pass


class ConvertImageDirNotFound(Exception):
    pass


class CanNotConvertImage(Exception):
    pass
    # print("請確認是否為影像檔及其影像格式")


class FormatNotSupport(Exception):
    pass


class OtherError(Exception):
    pass