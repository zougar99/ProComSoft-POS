"""
E-Commerce Platform Database Schema
PostgreSQL schema for scalable e-commerce application
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text,
    ForeignKey, JSON, ARRAY, Enum, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

Base = declarative_base()


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    STAFF = "staff"
    MANAGER = "manager"


# ============================================================================
# USER & AUTHENTICATION
# ============================================================================

class User(Base):
    """User accounts"""
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="user")
    
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
    )


class Address(Base):
    """User addresses"""
    __tablename__ = 'addresses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    type = Column(String(20))  # shipping, billing
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company = Column(String(255))
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    phone = Column(String(20))
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="shipping_address", foreign_keys="Order.shipping_address_id")
    
    __table_args__ = (
        Index('idx_address_user', 'user_id'),
    )


# ============================================================================
# PRODUCT CATALOG
# ============================================================================

class Category(Base):
    """Product categories"""
    __tablename__ = 'categories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Self-referential relationship
    children = relationship("Category", backref="parent", remote_side=[id])
    products = relationship("Product", back_populates="category")
    
    __table_args__ = (
        Index('idx_category_slug', 'slug'),
    )


class Brand(Base):
    """Product brands"""
    __tablename__ = 'brands'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="brand")


class Product(Base):
    """Products"""
    __tablename__ = 'products'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(Text)
    status = Column(String(20), default='draft')  # draft, active, archived
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'))
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float)
    cost_price = Column(Float)
    weight = Column(Float)
    dimensions = Column(JSON)  # {length, width, height}
    seo_title = Column(String(255))
    seo_description = Column(Text)
    meta_keywords = Column(ARRAY(String))
    is_featured = Column(Boolean, default=False)
    is_digital = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    
    __table_args__ = (
        Index('idx_product_sku', 'sku'),
        Index('idx_product_slug', 'slug'),
        Index('idx_product_status', 'status'),
        Index('idx_product_category', 'category_id'),
    )


class ProductVariant(Base):
    """Product variants (size, color, etc.)"""
    __tablename__ = 'product_variants'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    sku = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    price = Column(Float)
    compare_at_price = Column(Float)
    attributes = Column(JSON)  # {size: "L", color: "Red"}
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="variants")
    inventory = relationship("Inventory", back_populates="variant")
    cart_items = relationship("CartItem", back_populates="variant")
    order_items = relationship("OrderItem", back_populates="variant")
    
    __table_args__ = (
        Index('idx_variant_product', 'product_id'),
        Index('idx_variant_sku', 'sku'),
    )


class ProductImage(Base):
    """Product images"""
    __tablename__ = 'product_images'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey('product_variants.id'))
    url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    position = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="images")
    
    __table_args__ = (
        Index('idx_image_product', 'product_id'),
    )


class Inventory(Base):
    """Inventory tracking"""
    __tablename__ = 'inventory'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey('product_variants.id'))
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey('warehouses.id'))
    quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    reorder_point = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory")
    variant = relationship("ProductVariant", back_populates="inventory")
    warehouse = relationship("Warehouse", back_populates="inventory")
    
    __table_args__ = (
        Index('idx_inventory_product', 'product_id'),
        Index('idx_inventory_variant', 'variant_id'),
        Index('idx_inventory_warehouse', 'warehouse_id'),
        UniqueConstraint('product_id', 'variant_id', 'warehouse_id', name='unique_inventory'),
    )


class Warehouse(Base):
    """Warehouses"""
    __tablename__ = 'warehouses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    inventory = relationship("Inventory", back_populates="warehouse")


# ============================================================================
# SHOPPING CART
# ============================================================================

class CartItem(Base):
    """Shopping cart items"""
    __tablename__ = 'cart_items'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey('product_variants.id'))
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    variant = relationship("ProductVariant", back_populates="cart_items")
    
    __table_args__ = (
        Index('idx_cart_user', 'user_id'),
        UniqueConstraint('user_id', 'product_id', 'variant_id', name='unique_cart_item'),
    )


# ============================================================================
# ORDERS
# ============================================================================

class Order(Base):
    """Orders"""
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.id'))
    billing_address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.id'))
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0)
    shipping_amount = Column(Float, default=0)
    discount_amount = Column(Float, default=0)
    total = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")
    
    __table_args__ = (
        Index('idx_order_number', 'order_number'),
        Index('idx_order_user', 'user_id'),
        Index('idx_order_status', 'status'),
        Index('idx_order_created', 'created_at'),
    )


class OrderItem(Base):
    """Order line items"""
    __tablename__ = 'order_items'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey('product_variants.id'))
    sku = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    variant = relationship("ProductVariant", back_populates="order_items")
    
    __table_args__ = (
        Index('idx_order_item_order', 'order_id'),
    )


# ============================================================================
# PAYMENTS
# ============================================================================

class Payment(Base):
    """Payments"""
    __tablename__ = 'payments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    payment_method = Column(String(50), nullable=False)  # stripe, paypal, etc.
    payment_intent_id = Column(String(255))
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    transaction_id = Column(String(255))
    gateway_response = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    order = relationship("Order", back_populates="payments")
    
    __table_args__ = (
        Index('idx_payment_order', 'order_id'),
        Index('idx_payment_status', 'status'),
        Index('idx_payment_intent', 'payment_intent_id'),
    )


# ============================================================================
# SHIPPING
# ============================================================================

class Shipment(Base):
    """Shipments"""
    __tablename__ = 'shipments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    carrier = Column(String(50))  # fedex, ups, dhl, etc.
    tracking_number = Column(String(255), index=True)
    status = Column(String(50), default='pending')
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="shipments")
    
    __table_args__ = (
        Index('idx_shipment_order', 'order_id'),
        Index('idx_shipment_tracking', 'tracking_number'),
    )


# ============================================================================
# REVIEWS & RATINGS
# ============================================================================

class ProductReview(Base):
    """Product reviews"""
    __tablename__ = 'product_reviews'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255))
    review = Column(Text)
    is_verified_purchase = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    __table_args__ = (
        Index('idx_review_product', 'product_id'),
        Index('idx_review_user', 'user_id'),
        UniqueConstraint('product_id', 'user_id', 'order_id', name='unique_review'),
    )


# ============================================================================
# COUPONS & PROMOTIONS
# ============================================================================

class Coupon(Base):
    """Discount coupons"""
    __tablename__ = 'coupons'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    discount_type = Column(String(20))  # percentage, fixed_amount
    discount_value = Column(Float, nullable=False)
    minimum_purchase = Column(Float)
    maximum_discount = Column(Float)
    usage_limit = Column(Integer)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_coupon_code', 'code'),
    )

