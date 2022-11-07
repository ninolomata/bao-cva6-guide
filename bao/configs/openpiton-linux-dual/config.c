#include <config.h>

VM_IMAGE(linux_image, XSTR(/path/to/linux/lloader/linux-rv64-openpiton.bin));

struct config config = {
    
    CONFIG_HEADER

    .vmlist_size = 1,
    .vmlist = {
        { 
            .image = {
                .base_addr = 0x80200000,
                .load_addr = VM_IMAGE_OFFSET(linux_image),
                .size = VM_IMAGE_SIZE(linux_image)
            },

            .entry = 0x80200000,

            .platform = {
                .cpu_num = 2,
                
                .region_num = 1,
                .regions =  (struct mem_region[]) {
                    {
                        .base = 0x80200000,
                        .size = 0x20000000,
                    }
                },

                .dev_num = 2,
                .devs =  (struct dev_region[]) {
                    {
                        .pa = 0xfff0c2c000,   
                        .va = 0xfff0c2c000,  
                        .size = 0x000d4000,  
                        .interrupt_num = 1,
                        .interrupts = (uint64_t[]) {1}
                    },
                    {
                        .pa = 0xfff0d00000,   
                        .va = 0xfff0d00000,  
                        .size = 0x100000,  
                        .interrupt_num = 1,
                        .interrupts = (uint64_t[]) {2}
                    },
                },

                .arch = {
                   .plic_base = 0xfff1100000,
                }
            },
        }
     }
};