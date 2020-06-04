""" Module represents a User. """

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    ForeignKey
)

from sqlalchemy import (
    Column, String, Integer, DateTime, Date, Boolean, DECIMAL, ForeignKey, Text, Float
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, backref

from application.database import db
from application.database.model import CommonModel, default_uuid


################### USER - ROLE ###################
user_role = db.Table('user_role',
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('role_id', Integer, db.ForeignKey('role.id', ondelete='cascade'), primary_key=True))
###################################################

################### USER - FUNCTION ###################
user_function = db.Table('user_function',
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('function_id', Integer, db.ForeignKey('function.id', ondelete='cascade'), primary_key=True))
#######################################################

################### USER - LISTWORK ###################
user_listwork = db.Table('user_listwork',
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('listwork_id', Integer, db.ForeignKey('listwork.id', ondelete='cascade'), primary_key=True))
#######################################################

################### ROLE - FUNCTION ###################
role_function = db.Table('role_function',
                        db.Column('role_id', Integer, db.ForeignKey('role.id', ondelete='cascade'), primary_key=True),
                        db.Column('function_id', Integer, db.ForeignKey('function.id', ondelete='cascade'), primary_key=True))
#######################################################

################### EMPLOYEE - BRANCH ###################
employee_branch = db.Table('employee_branch',
                        db.Column('employee_id', Integer, db.ForeignKey('employee.id', ondelete='cascade'), primary_key=True),
                        db.Column('branch_id', Integer, db.ForeignKey('branch.id', ondelete='cascade'), primary_key=True))
#########################################################

################### EMPLOYEE - POSITION ###################
employee_position = db.Table('employee_position',
                        db.Column('employee_id', Integer, db.ForeignKey('employee.id', ondelete='cascade'), primary_key=True),
                        db.Column('position_id', Integer, db.ForeignKey('position.id', ondelete='cascade'), primary_key=True))
#########################################################

################### EMPLOYEE - SHIFT ###################
employee_shift = db.Table('employee_shift',
                        db.Column('employee_id', Integer, db.ForeignKey('employee.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
##################################################################

################### POSITION - SHIFT ###################
position_shift = db.Table('position_shift',
                        db.Column('position_id', Integer, db.ForeignKey('position.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
#########################################################

################### WORK - SHIFT ###################
work_shift = db.Table('work_shift',
                        db.Column('work__id', Integer, db.ForeignKey('work.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
####################################################

################### LISTWORK - WORK ###################
listwork_work = db.Table('listwork_work',
                        db.Column('listwork_id', Integer, db.ForeignKey('listwork.id', ondelete='cascade'), primary_key=True),
                        db.Column('work_id', Integer, db.ForeignKey('work.id', ondelete='cascade'), primary_key=True))
#########################################################



class User(CommonModel):
    __tablename__ = 'user'

    id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(String(255), nullable=False, unique=True)
    password = db.Column(String(255), nullable=False)
    salt = db.Column(String(255), nullable=False, unique=True)
    isActive = db.Column(Boolean, default=False)

    # CheckIn relationship
    checkin_id = db.Column(Integer, ForeignKey('checkin.id'))
    checkin = db.relationship("CheckIn", uselist=False, back_populates='user')

    # Employee relationship
    employee_id = db.Column(Integer, ForeignKey('employee.id'))
    employee = db.relationship("Employee", uselist=False, back_populates='user')

    # Role relationship
    role = db.relationship('Role', secondary=user_role, back_populates='user')

    # Function relationship
    function = db.relationship('Function', secondary=user_function, back_populates='user')

    # AssigningWork relationship
    assigningwork = db.relationship('AssigningWork', back_populates='user')

    # Examine relationship
    examine = db.relationship('Examine', back_populates='user')

    # Listwork relationship
    listwork = db.relationship('Listwork', back_populates='user')

class CheckIn(CommonModel):
    __tablename__ = 'checkin'

    id = db.Column(Integer, autoincrement=True, primary_key=True)

    # User relationship
    # user_id = db.Column(Integer, ForeignKey('user.id'))
    user = db.relationship("User", uselist=False, back_populates='checkin')

    time = db.Column(DateTime, nullable=False)
    is_checkin = db.Column(Boolean, default=False)
    is_late = db.Column(Boolean, default=True)

class Role(CommonModel):
    __tablename__ = 'role'

    id = db.Column(Integer, autoincrement=True, primary_key=True)
    role_name = db.Column(String(255), nullable=False, unique=True)

    # User relationship
    user = db.relationship('User', back_populates='role', secondary=user_role)

    # Function relationhsip
    function = db.relationship('Function', secondary=role_function, back_populates='role')


class Function(CommonModel):
    __tablename__ = 'function'

    id = db.Column(Integer, autoincrement=True, primary_key=True)
    function_name = db.Column(String(255), nullable=False, unique=True)

    # User relationship
    user = db.relationship('User', secondary=user_function, back_populates='function')

    # Role relationship
    role = db.relationship('Role', secondary=role_function, back_populates='function')



class Employee(CommonModel):
    __tablename__ = 'employee'

    id = db.Column(Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(String(255), nullable=False)
    date_birth = db.Column(Date)
    gender = db.Column(String(5), nullable=False)

    # Position relationship
    position = db.relationship("Position", secondary=employee_position, back_populates='employee')

    worked_time = db.Column(Integer, nullable=False)

    # KindOfStaff relationship
    kind_staff_id = db.Column(Integer, db.ForeignKey('kind_staff.id'))
    kind_staff = db.relationship("KindStaff", back_populates='employee')

    # # Available_Employee relationship
    # available_employee = db.relationship('Available_Employee', back_populates='employee')
    # available_employee_id = db.Column(Integer, ForeignKey('available_employee.id'))

    salary = db.Column(Integer, nullable=False)

    # User relationship
    user = db.relationship("User", back_populates='employee', uselist=False)
    user_id = db.Column(Integer, ForeignKey('user.id'))

    # Branch relationship
    branch = db.relationship('Branch', secondary=employee_branch, back_populates='employee')

    # Shift relationship
    shift = db.relationship('Shift', secondary=employee_shift, back_populates='employee')

# class Available_Employee(CommonModel):
#     __tablename__ = 'available_employee'
#     id = db.Column(Integer, autoincrement=True, primary_key=True)
#
#     # Employee relationship
#     employee = db.relationship("Employee", back_populates='available_employee')
#     employee_id = db.Column(Integer, ForeignKey('employee.id'))
#
#     # Shift relationship
#     shift = db.relationship("Shift", secondary=available_shift, back_populates='employee')
#

class Shift(CommonModel):
    __tablename__ = 'shift'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    shift_name = db.Column(String(255), nullable=False)
    start_time = db.Column(Date, nullable=False)
    end_time = db.Column(Date, nullable=False)

    # Employee relationship
    employee = db.relationship("Employee", secondary=employee_shift, back_populates='shift')

    # Position relationship
    position = db.relationship('Position', secondary=position_shift, back_populates='shift')

    # Work relationship
    work = db.relationship('Work', secondary=work_shift, back_populates='shift')

class Branch(CommonModel):
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    branch_name = db.Column(String(255), nullable=False)

    # Location relationship
    location = db.relationship("Location", back_populates='branch')
    location_id = db.Column(Integer, ForeignKey('location.id'))

    # Employee relationship
    employee = db.relationship('Employee', secondary=employee_branch, back_populates='branch')


class Position(CommonModel):
    __tablename__ = 'position'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    position_name = db.Column(String(255), nullable=False)

    # Employee relationship
    employee = db.relationship('Employee', secondary=employee_position, back_populates='position')
    # Shift relationship
    shift = db.relationship('Shift', secondary=position_shift, back_populates='position')

    # Work relationship
    work = db.relationship('Work', back_populates='position')


class Location(CommonModel):
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    street = db.Column(String(255), nullable=False)
    block = db.Column(String(255), nullable=False)
    district = db.Column(String(255), nullable=False)
    city = db.Column(String(255), nullable=False)
    nation = db.Column(String(255), nullable=False)

    # Branch relatioship
    branch = db.relationship("Branch", back_populates='location')



class Work(CommonModel):
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    name = db.Column(String(255), nullable=False)

    # Position relationship
    position = db.relationship('Position', back_populates='work')
    position_id = db.Column(Integer, ForeignKey('position.id'))

    # Shift relationship
    shift = db.relationship('Shift', secondary=work_shift, back_populates='work')

    start_time = db.Column(Date, nullable=False)
    end_time = db.Column(Date, nullable=False)
    description = db.Column(String(255))


class Listwork(CommonModel):
    __tablename__ = 'listwork'
    id = db.Column(Integer, autoincrement=True, primary_key=True)

    # AssigningWork relationship
    assigningwork = db.relationship('AssigningWork', back_populates='listwork')
    assigningwork_id = db.Column(Integer, ForeignKey('assigningwork.id'))

    # Examine relationship
    examine = db.relationship('Examine', back_populates='listwork')
    examine_id = db.Column(Integer, ForeignKey('examine.id'))

    # User relationship
    user = db.relationship('User', secondary=user_listwork, back_populates='listwork')

    start_time = db.Column(Date, nullable=False)
    end_time = db.Column(Date, nullable=False)
    description = db.Column(String(255))

class AssigningWork(CommonModel):
    __tablename__ = 'assigningwork'
    id = db.Column(Integer, autoincrement=True, primary_key=True)

    # User relationship (given_by)
    user = db.relationship('User', back_populates='assigningwork')
    given_by = db.Column(Integer, ForeignKey('user.id'), nullable=False)

    # User relationship (given to)
    given_to = db.Column(Integer, ForeignKey('user.id'), nullable=False)

class Examine(CommonModel):
    __tablename__ = 'examine'
    id = db.Column(Integer, autoincrement=True, primary_key=True)

    # User relationship
    user = db.relationship('User', back_populates='examine')
    examine_by = db.Column(Integer, ForeignKey('user.id'))

    isDone = db.Column(Boolean, default=False)

class KindStaff(CommonModel):
    __tablename__ = 'kind_staff'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    kind_name = db.Column(String(255), nullable=False)
    pay_rate = db.Column(Float, nullable=False)

    # Employee relationship
    employee = db.relationship("Employee", back_populates='kind_staff')



