-- MySQL 8.x schema for the campus canteen dataset
SET NAMES utf8mb4;

CREATE TABLE stalls (
  id INT UNSIGNED NOT NULL,
  name VARCHAR(80) NOT NULL,
  location VARCHAR(80) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_stalls_name (name),
  INDEX idx_stalls_location (location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE dishes (
  id INT UNSIGNED NOT NULL,
  stall_id INT UNSIGNED NOT NULL,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(40) NOT NULL,
  price DECIMAL(8,2) NOT NULL,
  portion_weight_g SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_dishes_stall_name (stall_id, name),
  INDEX idx_dishes_category (category),
  CHECK (price BETWEEN 3.00 AND 36.00),
  CHECK (portion_weight_g BETWEEN 150 AND 650),
  CONSTRAINT fk_dishes_stall FOREIGN KEY (stall_id) REFERENCES stalls(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE orders (
  id INT UNSIGNED NOT NULL,
  ordered_at DATETIME NOT NULL,
  meal_period ENUM('早餐','午餐','晚餐') NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_orders_time (ordered_at),
  INDEX idx_orders_meal_period (meal_period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE order_items (
  id INT UNSIGNED NOT NULL,
  order_id INT UNSIGNED NOT NULL,
  dish_id INT UNSIGNED NOT NULL,
  quantity TINYINT UNSIGNED NOT NULL,
  unit_price DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_order_items_order_dish (order_id, dish_id),
  INDEX idx_order_items_dish (dish_id),
  CHECK (quantity BETWEEN 1 AND 3),
  CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(id),
  CONSTRAINT fk_order_items_dish FOREIGN KEY (dish_id) REFERENCES dishes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE waste_records (
  id INT UNSIGNED NOT NULL,
  dish_id INT UNSIGNED NOT NULL,
  recorded_date DATE NOT NULL,
  waste_weight_g SMALLINT UNSIGNED NOT NULL,
  reason ENUM('备餐过量','制作失败','售后退回','临期报废','其他') NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_waste_dish_date (dish_id, recorded_date),
  INDEX idx_waste_weight (waste_weight_g),
  CHECK (waste_weight_g BETWEEN 1 AND 5000),
  CONSTRAINT fk_waste_dish FOREIGN KEY (dish_id) REFERENCES dishes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
