OS := $(shell uname)

SOURCE_DIR = ../src
BUILD_DIR = $(CURDIR)/build
LIB_DIR = $(BUILD_DIR)/debug
INCLUDE_DIR = ../include

INCS = -I$(INCLUDE_DIR)
CFLAGS = -I. -Wall -pedantic -fsanitize=address -g

ifeq ($(OS), Darwin)
CFLAGS += -framework Security
endif

LIBCRYPTO_DIR = $(dir $(shell find ${BUILD_DIR} -name libcrypto.a))
LIBSSL_DIR = $(dir $(shell find ${BUILD_DIR} -name libssl.a))

LDFLAGS = -L$(LIBCRYPTO_DIR) -L$(LIBSSL_DIR) -L$(LIB_DIR)

LIBS = -l:libquiche.a -lev -ldl -pthread

all: quic_client quic_server

quic_client: quic_client.c $(INCLUDE_DIR)/quiche.h $(LIB_DIR)/libquiche.a
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@ $(INCS) $(LIBS)

quic_server: quic_server.c $(INCLUDE_DIR)/quiche.h $(LIB_DIR)/libquiche.a
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@ $(INCS) $(LIBS)

$(LIB_DIR)/libquiche.a: $(SOURCE_DIR)/**/*.rs
	cd .. && cargo build --target-dir $(BUILD_DIR)

clean:
	@$(RM) -rf quic_server quic_client client server  build/
