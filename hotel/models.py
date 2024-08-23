from collections import defaultdict

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from hotel import db
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


class LoaiKH(db.Model):
    # __tablename__ = 'LoaiKH'
    maLKH = Column(Integer, primary_key=True, autoincrement=True)
    tenLKH = Column(String(50))
    kh = relationship('KhachHang', backref='loaikhachhang', lazy=True)

    def __str__(self):
        return self.name


class TaiKhoan(db.Model, UserMixin):
    # __tablename__ = 'TaiKhoan'
    maTK = Column(Integer, primary_key=True, autoincrement=True)
    tenTK = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    # 1-1
    # kh_id = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    kh = relationship('KhachHang', backref='tk', uselist=False, lazy=True)
    nv = relationship('NhanVien', backref='tk', uselist=False, lazy=True)
    nguoiqt = relationship('NguoiQuanTri', backref='tk',uselist=False, lazy=True)
    # kh_id = Column(Integer, ForeignKey('khachhang.maKH'), nullable=False)
    # avatar = Column(String(100),
    #                 default='static/images/deafaut.jpg')
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return str(self.maTK)


class NhanVien(db.Model):
    # __tablename__ = 'NhanVien'
    maNV = Column(Integer, primary_key=True, autoincrement=True)
    tenNV = Column(String(50))
    pdp = relationship('PhieuDatPhong', backref='NhanVien')
    ptp = relationship('PhieuThuePhong', backref='NhanVien')
    hd = relationship('HoaDon', backref='NhanVien')
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    def __str__(self):
        return self.name


class PhieuThuePhong(db.Model):
    # __tablename__ = 'PhieuThuePhong'
    maPTP = Column(Integer, primary_key=True, autoincrement=True)
    ngayNhanPhong = Column(DateTime)
    ngayTraPhong = Column(DateTime)
    phong = relationship('ChiTietPhieuThue', backref="phieuthuephong")
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    kh = relationship('KhachHang', backref='phieuthuephong')
    hd = relationship('HoaDon', backref='phieuthuephong')
    def __str__(self):
        return self.name


class PhieuDatPhong(db.Model):
    # __tablename__ = 'PhieuDatPhong'
    maPDP = Column(Integer, primary_key=True, autoincrement=True)
    ngayNhanPhong = Column(DateTime)
    ngayTraPhong = Column(DateTime)
    phong = relationship('ChiTietPhieuDat', backref="phieudatphong")
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    kh = relationship('KhachHang', backref='phieudatphong')

    def __str__(self):
        return self.name





class KhachHang(db.Model):
    # __tablename__ = 'KhachHang'
    maKH = Column(Integer, primary_key=True, autoincrement=True)
    hoTenKH = Column(String(50))
    diaChi = Column(String(100))
    soCCCD = Column(String(20))
    loaikh_id = Column(Integer, ForeignKey(LoaiKH.maLKH), nullable=False)
    hd = relationship('HoaDon', backref='kh', lazy=True)

    ptp_id = Column(Integer, ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    pdp_id = Column(Integer, ForeignKey(PhieuDatPhong.maPDP), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)

    def __str__(self):
        return self.hoTenKH

    def __str__(self):
        return self.maKH


class HoaDon(db.Model):
    # __tablename__ = 'HoaDon'
    maHD = Column(Integer, primary_key=True, autoincrement=True)
    ngayVao = Column(DateTime)
    ngayRa = Column(DateTime)
    kh_id = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    ptp = Column(Integer, ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    def __str__(self):
        return self.maHD


class LoaiPhong(db.Model):
    # __tablename__ = 'LoaiPhong'
    maLP = Column(Integer, primary_key=True, autoincrement=True)
    tenLP = Column(String(50), nullable=False, unique=True)
    phongs = relationship('Phong', backref='loaiphong', lazy=True)

    def __str__(self):
        return self.tenLP


class NguoiQuanTri(db.Model):
    # __tablename__ = 'NguoiQuanTri'
    maQT = Column(Integer, primary_key=True, autoincrement=True)
    tenQT = Column(String(50))
    phong = relationship('Phong', backref='nguoiQT', lazy=True)
    quydinh = relationship('QuyDinh', backref='nguoiQT', lazy=True)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    def __str__(self):
        return self.tenQT


# Phòng
class Phong(db.Model):
    # __tablename__ = 'Phong'
    maPhong = Column(Integer, primary_key=True, autoincrement=True)
    tenPhong = Column(String(50), nullable=False, unique=True)
    giaPhong = Column(Float, default=0)
    hinhAnh = Column(String(100))
    dienTich = Column(Float, default=0)
    # tinhTrang=Column(String(50))
    loaiphong_id = Column(Integer, ForeignKey(LoaiPhong.maLP), nullable=False)
    nguoiqt_id = Column(Integer, ForeignKey(NguoiQuanTri.maQT), nullable=False)
    # n-n
    ptp = relationship('ChiTietPhieuThue', backref='phong')
    pdp = relationship('ChiTietPhieuDat', backref='phong')

    receipt_details = relationship('ReceiptDetails', backref='phong', lazy=True)
    comments = relationship('Comment', backref='phong', lazy=True)

    def __str__(self):
        return self.tenPhong


class ChiTietPhieuThue(db.Model):
    # __tablename__ = 'ChiTietPTP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    left_id = Column(ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    right_id = Column(ForeignKey(Phong.maPhong), nullable=False)

    def __str__(self):
        return self.name


class ChiTietPhieuDat(db.Model):
    # __tablename__ = 'ChiTietPDP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    left_id = Column(ForeignKey(PhieuDatPhong.maPDP), nullable=False)
    right_id = Column(ForeignKey(Phong.maPhong), nullable=False)

    def __str__(self):
        return self.name


class QuyDinh(db.Model):
    # __tablename__ = 'QuyDinh'
    maQD = Column(Integer, primary_key=True, autoincrement=True)
    noiDungQD = Column(String(200))
    nguoiQT_id = Column(Integer, ForeignKey(NguoiQuanTri.maQT), nullable=False)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Phong.maPhong), nullable=False)


class Interaction(BaseModel):
    __abstract__ = True

    room_id = Column(Integer, ForeignKey(Phong.maPhong), nullable=False)
    user_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)


class Comment(Interaction):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    from hotel import app

    with app.app_context():
        db.create_all()

    # Thêm tài khoản admin
    #         import hashlib
    #
    #         u = TaiKhoan(tenTK='Admin',
    #                      username='admin',
    #                      password=str(hashlib.md5('1234567'.encode('utf-8')).hexdigest()),
    #                      user_role=UserRoleEnum.ADMIN)
    #
    #         db.session.add(u)
    #         db.session.commit()
    # Thêm người quản trị
    #     qt1 = NguoiQuanTri(tenQT='admin1', tk_id = 1)
    #
    #     db.session.add(qt1)
    #     db.session.commit()
#
#     # Thêm loại phòng
#         l1 = LoaiPhong(tenLP='Phòng đôi')
#         l2 = LoaiPhong(tenLP='Phòng đơn')
#
#         db.session.add(l1)
#         db.session.add(l2)
#         db.session.commit()
#
#     #Thêm nhân viên
#         nv1 = NhanVien(tenNV='Y Vy', tk_id = 5)
#         db.session.add(nv1)
#         db.session.commit()

#
#     # Thêm phòng
#         p1 = Phong(tenPhong='Phòng đơn', giaPhong=250000,
#                    hinhAnh="images/img_3.jpg",
#                    dienTich=20,
#                    loaiphong_id=1,
#                    nguoiqt_id=2)
#
#         p2 = Phong(tenPhong='Phòng đôi ', giaPhong=350000,
#                    hinhAnh="images/img_1.jpg",
#                    dienTich=27.0,
#                    loaiphong_id=2,
#                    nguoiqt_id=2)
#         p3 = Phong(tenPhong='Phòng gia đình', giaPhong=500000,
#                    hinhAnh="images/img_2.jpg",
#                    dienTich=40.5,
#                    loaiphong_id=2,
#                    nguoiqt_id=2)
#         p4 = Phong(tenPhong='Phòng cao cấp ', giaPhong=400000,
#                    hinhAnh="images/img_4.jpg",
#                    dienTich=30,
#                    loaiphong_id=2,
#                    nguoiqt_id=2)
#
#
#         db.session.add_all([p1,p2, p3, p4])
#         db.session.commit()
#
#     # Thêm loại khách hàng
#         kh1 = LoaiKH(tenLKH='Trong nước')
#         kh2 = LoaiKH(tenLKH='Nước ngoài')
#         db.session.add(kh1)
#         db.session.add(kh2)
#         db.session.commit()
#
#

        # import hashlib
        #
        # u = TaiKhoan(tenTK='Nam Phuong',
        #              username='ntnp',
        #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #              user_role=UserRoleEnum.USER)
        #
        # db.session.add(u)
        # db.session.commit()
        # import hashlib
        #
        # u = TaiKhoan(tenTK='Thanh Truc',
        #              username='ttt',
        #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #              user_role=UserRoleEnum.USER)
        #
        # db.session.add(u)
        # db.session.commit()
        # import hashlib
        #
        # u = TaiKhoan(tenTK='Truc Tran',
        #              username='trantruc',
        #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #              user_role=UserRoleEnum.USER)
        #
        # db.session.add(u)
        # db.session.commit()
# # Phiếu đặt phòng
#         pdp1 = PhieuDatPhong(ngayNhanPhong='2024-1-1', ngayTraPhong='2024-1-2',
#                             nv_id=1)
#         db.session.add(pdp1)
#         db.session.commit()





