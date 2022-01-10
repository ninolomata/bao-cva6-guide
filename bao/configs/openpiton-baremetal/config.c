#include <config.h>

VM_IMAGE(baremetal_image, XSTR(/path/to/bao-baremetal-guest/build/openpiton/baremetal.bin));

struct config config = {
    
    CONFIG_HEADER

    .vmlist_size = 1,
    .vmlist = {
        { 
            .image = {
                .base_addr = 0x80200000,
                .load_addr = VM_IMAGE_OFFSET(baremetal_image),
                .size = VM_IMAGE_SIZE(baremetal_image)
            },

            .entry = 0x80200000,

            .platform = {
                .cpu_num = 1,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x80200000,
                        .size = 0x1000000 //128MB
                    }
                },

                .dev_num = 1,
                .devs =  (struct dev_region[]) {
                    {
                        .pa = 0xfff0c2c000,   
                        .va = 0xfff0c2c000,  
                        .size = 0x000d4000,  
                        .interrupt_num = 1,
                        .interrupts = (uint64_t[]) {1}
                    },
                },

                .arch = {
                   .plic_base = 0xfff1100000,
                }
            },
        }
    }
};