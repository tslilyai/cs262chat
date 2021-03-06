# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service.proto',
  package='chatapp',
  syntax='proto3',
  serialized_pb=_b('\n\rservice.proto\x12\x07\x63hatapp\"G\n\x08\x43Message\x12\x0c\n\x04m_id\x18\x01 \x01(\x03\x12\r\n\x05to_id\x18\x02 \x01(\x03\x12\x11\n\tfrom_name\x18\x03 \x01(\t\x12\x0b\n\x03msg\x18\x04 \x01(\t\"L\n\x04User\x12\x0c\n\x04u_id\x18\x01 \x01(\x03\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x12\n\ncheckpoint\x18\x04 \x01(\x03\"0\n\x08UserPair\x12\x11\n\tusername1\x18\x01 \x01(\t\x12\x11\n\tusername2\x18\x02 \x01(\t\"Q\n\x05Group\x12\x0c\n\x04g_id\x18\x01 \x01(\x03\x12\x0e\n\x06g_name\x18\x02 \x01(\t\x12\x18\n\x10\x65\x64it_member_name\x18\x04 \x01(\t\x12\x10\n\x08new_name\x18\x05 \x01(\t\"&\n\x08Response\x12\r\n\x05\x65rrno\x18\x01 \x01(\x05\x12\x0b\n\x03msg\x18\x02 \x01(\t\"\x1a\n\x07Pattern\x12\x0f\n\x07pattern\x18\x01 \x01(\t2\xce\x05\n\x07\x43hatApp\x12:\n\x10rpc_send_message\x12\x11.chatapp.CMessage\x1a\x11.chatapp.Response\"\x00\x12\x38\n\x10rpc_get_messages\x12\r.chatapp.User\x1a\x11.chatapp.CMessage\"\x00\x30\x01\x12>\n\x17rpc_create_conversation\x12\x11.chatapp.UserPair\x1a\x0e.chatapp.Group\"\x00\x12\x34\n\x10rpc_create_group\x12\x0e.chatapp.Group\x1a\x0e.chatapp.Group\"\x00\x12\x34\n\x12rpc_create_account\x12\r.chatapp.User\x1a\r.chatapp.User\"\x00\x12\x38\n\x12rpc_remove_account\x12\r.chatapp.User\x1a\x11.chatapp.Response\"\x00\x12:\n\x13rpc_edit_group_name\x12\x0e.chatapp.Group\x1a\x11.chatapp.Response\"\x00\x12>\n\x17rpc_remove_group_member\x12\x0e.chatapp.Group\x1a\x11.chatapp.Response\"\x00\x12;\n\x14rpc_add_group_member\x12\x0e.chatapp.Group\x1a\x11.chatapp.Response\"\x00\x12;\n\x16rpc_list_group_members\x12\x0e.chatapp.Group\x1a\r.chatapp.User\"\x00\x30\x01\x12\x37\n\x0frpc_list_groups\x12\x10.chatapp.Pattern\x1a\x0e.chatapp.Group\"\x00\x30\x01\x12\x38\n\x11rpc_list_accounts\x12\x10.chatapp.Pattern\x1a\r.chatapp.User\"\x00\x30\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_CMESSAGE = _descriptor.Descriptor(
  name='CMessage',
  full_name='chatapp.CMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='m_id', full_name='chatapp.CMessage.m_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='to_id', full_name='chatapp.CMessage.to_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='from_name', full_name='chatapp.CMessage.from_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='chatapp.CMessage.msg', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=97,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='chatapp.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='u_id', full_name='chatapp.User.u_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username', full_name='chatapp.User.username', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='password', full_name='chatapp.User.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='checkpoint', full_name='chatapp.User.checkpoint', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=99,
  serialized_end=175,
)


_USERPAIR = _descriptor.Descriptor(
  name='UserPair',
  full_name='chatapp.UserPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username1', full_name='chatapp.UserPair.username1', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='username2', full_name='chatapp.UserPair.username2', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=225,
)


_GROUP = _descriptor.Descriptor(
  name='Group',
  full_name='chatapp.Group',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='g_id', full_name='chatapp.Group.g_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='g_name', full_name='chatapp.Group.g_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='edit_member_name', full_name='chatapp.Group.edit_member_name', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='new_name', full_name='chatapp.Group.new_name', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=227,
  serialized_end=308,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='chatapp.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errno', full_name='chatapp.Response.errno', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='msg', full_name='chatapp.Response.msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=348,
)


_PATTERN = _descriptor.Descriptor(
  name='Pattern',
  full_name='chatapp.Pattern',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pattern', full_name='chatapp.Pattern.pattern', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=350,
  serialized_end=376,
)

DESCRIPTOR.message_types_by_name['CMessage'] = _CMESSAGE
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['UserPair'] = _USERPAIR
DESCRIPTOR.message_types_by_name['Group'] = _GROUP
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['Pattern'] = _PATTERN

CMessage = _reflection.GeneratedProtocolMessageType('CMessage', (_message.Message,), dict(
  DESCRIPTOR = _CMESSAGE,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.CMessage)
  ))
_sym_db.RegisterMessage(CMessage)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), dict(
  DESCRIPTOR = _USER,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.User)
  ))
_sym_db.RegisterMessage(User)

UserPair = _reflection.GeneratedProtocolMessageType('UserPair', (_message.Message,), dict(
  DESCRIPTOR = _USERPAIR,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.UserPair)
  ))
_sym_db.RegisterMessage(UserPair)

Group = _reflection.GeneratedProtocolMessageType('Group', (_message.Message,), dict(
  DESCRIPTOR = _GROUP,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.Group)
  ))
_sym_db.RegisterMessage(Group)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.Response)
  ))
_sym_db.RegisterMessage(Response)

Pattern = _reflection.GeneratedProtocolMessageType('Pattern', (_message.Message,), dict(
  DESCRIPTOR = _PATTERN,
  __module__ = 'service_pb2'
  # @@protoc_insertion_point(class_scope:chatapp.Pattern)
  ))
_sym_db.RegisterMessage(Pattern)


import abc
from grpc.beta import implementations as beta_implementations
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

class BetaChatAppServicer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def rpc_send_message(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_get_messages(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_create_conversation(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_create_group(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_create_account(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_remove_account(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_edit_group_name(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_remove_group_member(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_add_group_member(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_list_group_members(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_list_groups(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_list_accounts(self, request, context):
    raise NotImplementedError()

class BetaChatAppStub(object):
  """The interface to which stubs will conform."""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def rpc_send_message(self, request, timeout):
    raise NotImplementedError()
  rpc_send_message.future = None
  @abc.abstractmethod
  def rpc_get_messages(self, request, timeout):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_create_conversation(self, request, timeout):
    raise NotImplementedError()
  rpc_create_conversation.future = None
  @abc.abstractmethod
  def rpc_create_group(self, request, timeout):
    raise NotImplementedError()
  rpc_create_group.future = None
  @abc.abstractmethod
  def rpc_create_account(self, request, timeout):
    raise NotImplementedError()
  rpc_create_account.future = None
  @abc.abstractmethod
  def rpc_remove_account(self, request, timeout):
    raise NotImplementedError()
  rpc_remove_account.future = None
  @abc.abstractmethod
  def rpc_edit_group_name(self, request, timeout):
    raise NotImplementedError()
  rpc_edit_group_name.future = None
  @abc.abstractmethod
  def rpc_remove_group_member(self, request, timeout):
    raise NotImplementedError()
  rpc_remove_group_member.future = None
  @abc.abstractmethod
  def rpc_add_group_member(self, request, timeout):
    raise NotImplementedError()
  rpc_add_group_member.future = None
  @abc.abstractmethod
  def rpc_list_group_members(self, request, timeout):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_list_groups(self, request, timeout):
    raise NotImplementedError()
  @abc.abstractmethod
  def rpc_list_accounts(self, request, timeout):
    raise NotImplementedError()

def beta_create_ChatApp_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  request_deserializers = {
    ('chatapp.ChatApp', 'rpc_add_group_member'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_create_account'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_create_conversation'): service_pb2.UserPair.FromString,
    ('chatapp.ChatApp', 'rpc_create_group'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_edit_group_name'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_get_messages'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_list_accounts'): service_pb2.Pattern.FromString,
    ('chatapp.ChatApp', 'rpc_list_group_members'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_list_groups'): service_pb2.Pattern.FromString,
    ('chatapp.ChatApp', 'rpc_remove_account'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_remove_group_member'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_send_message'): service_pb2.CMessage.FromString,
  }
  response_serializers = {
    ('chatapp.ChatApp', 'rpc_add_group_member'): service_pb2.Response.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_account'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_conversation'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_group'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_edit_group_name'): service_pb2.Response.SerializeToString,
    ('chatapp.ChatApp', 'rpc_get_messages'): service_pb2.CMessage.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_accounts'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_group_members'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_groups'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_remove_account'): service_pb2.Response.SerializeToString,
    ('chatapp.ChatApp', 'rpc_remove_group_member'): service_pb2.Response.SerializeToString,
    ('chatapp.ChatApp', 'rpc_send_message'): service_pb2.Response.SerializeToString,
  }
  method_implementations = {
    ('chatapp.ChatApp', 'rpc_add_group_member'): face_utilities.unary_unary_inline(servicer.rpc_add_group_member),
    ('chatapp.ChatApp', 'rpc_create_account'): face_utilities.unary_unary_inline(servicer.rpc_create_account),
    ('chatapp.ChatApp', 'rpc_create_conversation'): face_utilities.unary_unary_inline(servicer.rpc_create_conversation),
    ('chatapp.ChatApp', 'rpc_create_group'): face_utilities.unary_unary_inline(servicer.rpc_create_group),
    ('chatapp.ChatApp', 'rpc_edit_group_name'): face_utilities.unary_unary_inline(servicer.rpc_edit_group_name),
    ('chatapp.ChatApp', 'rpc_get_messages'): face_utilities.unary_stream_inline(servicer.rpc_get_messages),
    ('chatapp.ChatApp', 'rpc_list_accounts'): face_utilities.unary_stream_inline(servicer.rpc_list_accounts),
    ('chatapp.ChatApp', 'rpc_list_group_members'): face_utilities.unary_stream_inline(servicer.rpc_list_group_members),
    ('chatapp.ChatApp', 'rpc_list_groups'): face_utilities.unary_stream_inline(servicer.rpc_list_groups),
    ('chatapp.ChatApp', 'rpc_remove_account'): face_utilities.unary_unary_inline(servicer.rpc_remove_account),
    ('chatapp.ChatApp', 'rpc_remove_group_member'): face_utilities.unary_unary_inline(servicer.rpc_remove_group_member),
    ('chatapp.ChatApp', 'rpc_send_message'): face_utilities.unary_unary_inline(servicer.rpc_send_message),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

def beta_create_ChatApp_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  import service_pb2
  request_serializers = {
    ('chatapp.ChatApp', 'rpc_add_group_member'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_account'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_conversation'): service_pb2.UserPair.SerializeToString,
    ('chatapp.ChatApp', 'rpc_create_group'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_edit_group_name'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_get_messages'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_accounts'): service_pb2.Pattern.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_group_members'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_list_groups'): service_pb2.Pattern.SerializeToString,
    ('chatapp.ChatApp', 'rpc_remove_account'): service_pb2.User.SerializeToString,
    ('chatapp.ChatApp', 'rpc_remove_group_member'): service_pb2.Group.SerializeToString,
    ('chatapp.ChatApp', 'rpc_send_message'): service_pb2.CMessage.SerializeToString,
  }
  response_deserializers = {
    ('chatapp.ChatApp', 'rpc_add_group_member'): service_pb2.Response.FromString,
    ('chatapp.ChatApp', 'rpc_create_account'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_create_conversation'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_create_group'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_edit_group_name'): service_pb2.Response.FromString,
    ('chatapp.ChatApp', 'rpc_get_messages'): service_pb2.CMessage.FromString,
    ('chatapp.ChatApp', 'rpc_list_accounts'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_list_group_members'): service_pb2.User.FromString,
    ('chatapp.ChatApp', 'rpc_list_groups'): service_pb2.Group.FromString,
    ('chatapp.ChatApp', 'rpc_remove_account'): service_pb2.Response.FromString,
    ('chatapp.ChatApp', 'rpc_remove_group_member'): service_pb2.Response.FromString,
    ('chatapp.ChatApp', 'rpc_send_message'): service_pb2.Response.FromString,
  }
  cardinalities = {
    'rpc_add_group_member': cardinality.Cardinality.UNARY_UNARY,
    'rpc_create_account': cardinality.Cardinality.UNARY_UNARY,
    'rpc_create_conversation': cardinality.Cardinality.UNARY_UNARY,
    'rpc_create_group': cardinality.Cardinality.UNARY_UNARY,
    'rpc_edit_group_name': cardinality.Cardinality.UNARY_UNARY,
    'rpc_get_messages': cardinality.Cardinality.UNARY_STREAM,
    'rpc_list_accounts': cardinality.Cardinality.UNARY_STREAM,
    'rpc_list_group_members': cardinality.Cardinality.UNARY_STREAM,
    'rpc_list_groups': cardinality.Cardinality.UNARY_STREAM,
    'rpc_remove_account': cardinality.Cardinality.UNARY_UNARY,
    'rpc_remove_group_member': cardinality.Cardinality.UNARY_UNARY,
    'rpc_send_message': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'chatapp.ChatApp', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)
