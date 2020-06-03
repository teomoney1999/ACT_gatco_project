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

roles_users = db.Table('roles_users',
                       db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                       db.Column('role_id', Integer, db.ForeignKey('role.id', onupdate='cascade'), primary_key=True))


class User(CommonModel): 
    __tablename__ = 'user'

    id = db.Column(Integer, autogenerate=True, primary_key=True)
    user_name = db.Column(String(255), nullable=False, unique=True)
    password = db.Column(String(255), nullable=False)
    salt = db.Column(String(255), nullable=False, unique=True)
    isActive = db.Column(Boolean, default=False)
    
    # CheckIn relationship 
    checkin_id = db.Column(Integer, ForeignKey('checkin.id'))
    checkin = db.relationship("CheckIn", uselist=False, back_populates='user')

    # Employee relationship 
    employee_id = db.Column(Integer, ForeignKey('staff.id'))
    empolyee = db.relationship("Employee", uselist=False, back_populates='user')

    # Role relationship
    role = db.relationship('Role', secondary='user_role', back_populates='user')

    # Function relationship
    function = db.relationship('Function', secondary='user_function', back_populates='user')

    # Assigning_Work relationship
    assigning_work = db.relationship('Assigning_Work', back_populates='user')

    # Examine relationship 
    examine = db.relationship('Examine', back_populates='user')

    # List_Work relationship 
    list_work = db.relationship('List_Work', back_populates='user')

class CheckIn(CommonModel): 
    __tablename__ = 'checkin'

    id = db.Column(Integer, autogenerate=True, primary_key=True)
     
    # User relationship
    user_id = db.Column(Integer, ForeignKey('user.id'))
    user = db.relationship("User", uselist=False, back_populates='checkin')

    time = db.Column(DateTime, nullable=False)
    isCheckin = db.Column(Boolean, default=False)
    isLate = db.Column(Boolean, default=True)

class Role(CommonModel): 
    __tablename__ = 'role'

    id = db.Column(Integer, autogenerate=True, primary_key=True)
    role_name = db.Column(String(255), nullable=False, unique=True)

    # User relationship
    user = db.relationship('User', back_populates='role', secondary='user_role')

    # Function relationhsip
    function = db.relationship('Function', back_populates='role', secondary='role_function')

################### USER - ROLE ###################
user_role = db.Table('user_role', 
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('role_id', Integer, db.ForeignKey('role.id', ondelete='cascade'), primary_key=True))
###################################################

class Function(CommonModel): 
    __tablename__ = 'function'

    id = db.Column(Integer, autogenerate=True, primary_key=True)
    function_name = db.Column(String(255), nullable=False, unique=True)

    # User relationship
    user = db.relationship('User', secondary='user_function', back_populates='function')

    # Role relationship
    role = db.relationship('Role', secondary='role_function', back_populates='function')

################### USER - FUNCTION ###################
user_function = db.Table('user_function', 
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('function_id', Integer, db.ForeignKey('function.id', ondelete='cascade'), primary_key=True))
#######################################################

################### ROLE - FUNCTION ###################
role_function = db.Table('role_function', 
                        db.Column('role_id', Integer, db.ForeignKey('role.id', ondelete='cascade'), primary_key=True),
                        db.Column('function_id', Integer, db.ForeignKey('function.id', ondelete='cascade'), primary_key=True))
#######################################################

class Employee(CommonModel): 
    __tablename__ = 'employee'

    id = db.Column(Integer, autogenerate=True, primary_key=True)
    full_name = db.Column(String(255), nullable=False)
    date_birth = db.Column(Date)
    gender = db.Column(String(5), nullabl=False)

    # Position relationship
    position = db.relationship("Position", back_populates='employee')

    worked_time = db.Column(Integer, nullable=False)
    # KindOfStaff relationship
    kind_staff = db.relationship("Employee", back_populates='employee')
    kind_staff_id = db.Column(Integer, ForeignKey('kind_staff.id'))

    # Available_Employee relationship 
    available_employee = db.relationship('Available_Employee', back_populates='employee')
    available_employee_id = db.Column(Integer, ForeignKey('available_employee.id'))

    salary = db.Column(Integer, nullabale=False)

    # User relationship
    user = db.relationship("User", back_populates='employee', uselist=False)
    user_id = db.Column(Integer, ForeignKey('user.id'))

class Available_Employee(CommonModel): 
    __tablename__ = 'available_employee'
    id = db.Column(Integer, autogenerate=True, primary_key=True)

    # Employee relationship
    employee = db.relationship("Employee", back_populates='available_employee')
    employee_id = db.Column(Integer, ForeignKey('employee.id'))

    # Shift relationship
    shift = db.relationship("Shift", secondary='available_shift', back_populates='employee')

################### AVAILABLE_EMPLOYEE - SHIFT ###################
available_shift = db.Table('available_shift', 
                        db.Column('available_employee_id', Integer, db.ForeignKey('available_employee.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
##################################################################

class Shift(CommonModel): 
    __tablename__ = 'shift'
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    shift_name = db.Column(String(255), nullable=False)
    start_time = db.Column(Date, nullable=False) 
    end_time = db.Column(Date, nullable=False)

    # Employee relationship
    employee = db.relationship("Employee", secondary='available_shift', back_populates='shift')

    # Position relationship
    position = db.relationship('Position', secondary='position_shift', back_populates='shift')

    # Work relationship
    work = db.relationship('Work', secondary='work_shift', back_populates='shift')

class Branch(CommonModel): 
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    branch_name = db.Column(String(255), nullable=False)

    # Location relationship
    location = db.relationship("Location", back_populates='branch')
    location_id = db.Column(Integer, ForeignKey('location.id'))

################### EMPLOYEE - BRANCH ###################
employee_branch = db.Table('employee_branch', 
                        db.Column('employee_id', Integer, db.ForeignKey('employee.id', ondelete='cascade'), primary_key=True),
                        db.Column('branch_id', Integer, db.ForeignKey('branch.id', ondelete='cascade'), primary_key=True))
#########################################################

################### POSITION - SHIFT ###################
position_shift = db.Table('position_shift', 
                        db.Column('position_id', Integer, db.ForeignKey('position.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
#########################################################

class Position(CommonModel):
    __tablename__ = 'position' 
    id = db.Column(Integer, autogenerate=True, primary_key=True) 
    position_name = db.Column(String(255), nullable=False) 

    # Shift relationship 
    shift = db.relationship('Shift', secondary='position_shift', back_populates='position')


class Location(CommonModel): 
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    street = db.Column(String(255), nullable=False)
    block = db.Column(String(255), nullable=False)
    district = db.Column(String(255), nullable=False)
    city = db.Column(String(255), nullable=False)
    nation = db.Column(String(255), nullable=False)

    # Branch relatioship
    branch = db.relationship("Branch", back_populates='location')

################### LISTWORK - WORK ###################
listwork_work = db.Table('listwork_work', 
                        db.Column('list_work_id', Integer, db.ForeignKey('list_work.id', ondelete='cascade'), primary_key=True),
                        db.Column('work_id', Integer, db.ForeignKey('work.id', ondelete='cascade'), primary_key=True))
#########################################################

class Work(CommonModel): 
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    name = db.Column(String(255), nullable=False)

    # Position relationship
    position = db.relationship('Position', back_populates='work')
    position_id = db.Column(Integer, ForeignKey('position.id'))

    # Shift relationship 
    shift = db.relationship('Shift', secondary='listwork_shift', back_populates='work')

    start_time = db.Column(Date, nullable=False)
    end_time = db.Column(Date, nullable=False)
    description = db.Column(String(255))

################### USER - LISTWORK ###################
user_listwork = db.Table('user_listwork', 
                        db.Column('user_id', Integer, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                        db.Column('list_work_id', Integer, db.ForeignKey('list_work.id', ondelete='cascade'), primary_key=True))
#######################################################

################### WORK - SHIFT ###################
work_shift = db.Table('work_shift', 
                        db.Column('work__id', Integer, db.ForeignKey('work.id', ondelete='cascade'), primary_key=True),
                        db.Column('shift_id', Integer, db.ForeignKey('shift.id', ondelete='cascade'), primary_key=True))
####################################################
class List_Work(CommonModel): 
    __tablename__ = 'list_work'
    id = db.Column(Integer, autogenerate=True, primary_key=True)

    # Assigning_Work relationship 
    assigning_work = db.relationship('Assigning_Work', back_populates='list_work')
    assigning_work_id = db.Column(Integer, ForeignKey('assigning_work.id'))

    # Examine relationship 
    examine = db.relationship('Examine', back_populates='list_work')
    examine_id = db.Column(Integer, ForeignKey('examine.id'))

    # User relationship
    user = db.Column('User', secondary='user_listwork', back_populates='list_work')

    start_time = db.Column(Date, nullable=False)
    end_time = db.Column(Date, nullable=False)
    description = db.Column(String(255))

class Assigning_Work(CommonModel): 
    __tablename__ = 'assigning_work' 
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    # User relationship (given_by)
    user = db.relationship('User', back_populates='assigning_work') 
    given_by = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    # User relationship (given to)
    given_to = db.Column(Integer, ForeignKey('user.id'), nullable=False)

class Examine(CommonModel):
    __tablename__ = 'examine' 
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    
    # User relationship 
    user = db.relationship('User', back_populates='examine') 
    examine_by = db.Column(Integer, ForeignKey('user.id'))

    isDone = db.Column(Boolean, default=False)

class KindStaff(CommonModel): 
    __tablename__ = 'kind_staff'
    id = db.Column(Integer, autogenerate=True, primary_key=True)
    kind_name = db.Column(String(255), nullable=False)
    pay_rate = db.Column(Float, nullable=False)

    # Employee relationship
    employee = db.relationship("Employee", back_populates='kind_staff')


    
