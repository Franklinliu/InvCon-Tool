package daikon.derive.senary;

import daikon.ValueTuple;
import daikon.VarInfo;
import daikon.derive.Derivation;
import daikon.derive.ValueAndModified;
import org.plumelib.util.ArraysPlume;
import org.plumelib.util.Intern;

import org.checkerframework.dataflow.qual.SideEffectFree;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.checker.interning.qual.Interned;

public final class InvConUserBookkeepingBigInt2 extends SenaryDerivation {
    // We are Serializable, so we specify a version to allow changes to
    // method signatures without breaking serialization.  If you add or
    // remove fields, you should change this number to the current date.
    static final long serialVersionUID = 20101004L;

    // Variables starting with dkconfig_ should only be set via the
    // daikon.config.Configuration interface.
    /** Boolean. True iff InvConUserBalance derived variables should be generated. */
    public static boolean dkconfig_enabled = false;

    protected InvConUserBookkeepingBigInt2(VarInfo vi1, VarInfo vi2, VarInfo vi3, VarInfo vi4, VarInfo vi5,VarInfo vi6) {
        super(vi1, vi2, vi3, vi4, vi5, vi6);
        //TODO Auto-generated constructor stub
    }

    public VarInfo main_keys_var() {
        return base1;
    }

    public VarInfo sub_keys_var() {
        return base2;
    }

    public VarInfo sub_lengths_var() {
        return base3;
    }

    public VarInfo values_var() {
        return base4;
    }

    public VarInfo key_var1() {
        return base5;
    }

    public VarInfo key_var2() {
        return base6;
    }

    @Override
    public ValueAndModified computeValueAndModified(ValueTuple full_vt) {
        // TODO Auto-generated method stub
        int mod1 = base1.getModified(full_vt);
        if (mod1 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod2 = base2.getModified(full_vt);
        if (mod2 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod3 = base3.getModified(full_vt);
        if (mod3 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }

        int mod4 = base4.getModified(full_vt);
        if (mod4 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod5 = base5.getModified(full_vt);
        if (mod5 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod6 = base6.getModified(full_vt);
        if (mod6 == ValueTuple.MISSING_NONSENSICAL) {
          return ValueAndModified.MISSING_NONSENSICAL;
        }
        int mod =
        (((mod1 == ValueTuple.UNMODIFIED)
          && (mod2 == ValueTuple.UNMODIFIED)
          && (mod3 == ValueTuple.UNMODIFIED)
          && (mod4 == ValueTuple.UNMODIFIED)
          && (mod5 == ValueTuple.UNMODIFIED)
          && (mod6 == ValueTuple.UNMODIFIED)
         )
         ? ValueTuple.UNMODIFIED
         : ValueTuple.MODIFIED);

        String[] val1_array  = main_keys_var().getStringArrayValue(full_vt);
        if (val1_array == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        for (int i=0; i< val1_array.length; i++){
            val1_array[i] = val1_array[i].toLowerCase();
        }

        String[] val2_array  = sub_keys_var().getStringArrayValue(full_vt);
        if (val2_array == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        for (int i=0; i< val2_array.length; i++){
            val2_array[i] = val2_array[i].toLowerCase();
        }

     
        // System.out.printf("sub_lengths_var().name(): %s", sub_lengths_var().name());
        long[] val3_array = sub_lengths_var().getIntArrayValue(full_vt);
        if (val3_array == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        Object val4 = values_var().getValue(full_vt);
        if (val4 == null) {
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        java.math.BigInteger[] val4_array = (java.math.BigInteger[]) val4;
     
        String key_var1 = key_var1().getStringValue(full_vt);
        String key_var2 = key_var2().getStringValue(full_vt);
        if (key_var1 == null || key_var2 == null){
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        
        key_var1 = key_var1.toLowerCase();
        key_var2 = key_var2.toLowerCase();

        // len(main_keys_var) ==  len(sub_lengths_var)
        if (val1_array.length != val3_array.length){
            return ValueAndModified.MISSING_NONSENSICAL;
        }
        
        long sum = 0;
        for (long len: val3_array){
            sum += len;
        }
        // SUM(sub_lengths_var) ==  len(sub_keys_var) == len(values_var)
        if (sum != val2_array.length || sum != val4_array.length){
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        if (val1_array.length == 0){
            // return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
            return ValueAndModified.MISSING_NONSENSICAL;
        }

        // (1) key_var1 is main key, key_var2 is sub key
        // (2) key_var2 is main key, key_var1 is sub key
        // Suppose (1) since we believe Daikon will iterate all combinations
                
        // int key_var1_index = ArraysPlume.indexOf(val1_array, key_var1);
        int key_var1_index = ArraysPlume.indexOf(val1_array, key_var1);

        int key_var2_index = ArraysPlume.indexOf(val1_array, key_var2);

        System.out.printf("InvConUserBookkeeping2 name: %s, key_val:%s exist: %b\n", this.getVarInfo().name(),  key_var2, key_var2_index!=-1);

        if (key_var1_index==-1 && key_var2_index == -1){
            // return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
            return ValueAndModified.MISSING_NONSENSICAL;
        }else if(key_var1_index!=-1){
            long sub_key_size = val3_array[key_var1_index];
            long sub_key_start_index = 0;
            for (int i=0; i<key_var1_index; i++){
                sub_key_start_index +=  val3_array[i];
            }
            // find sub key index in the array sub_keys_var
            // int index = ArraysPlume.indexOf(val2_array, key_var2, sub_key_start_index, sub_key_start_index+sub_key_size);
            int index = -1;
            for (long i= sub_key_start_index; i< sub_key_start_index+sub_key_size;i++){
                if (val2_array[(int)i].equals(key_var2)){
                    index = (int)i;
                    break;
                }
            }

            if (index==-1){
                // double val = 0;
                // return new ValueAndModified(val, ValueTuple.UNMODIFIED);
                // return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                return ValueAndModified.MISSING_NONSENSICAL;
            }
            // get values_var[index]
            java.math.BigInteger val = val4_array[index];
            String val_string = Intern.intern(val.toString());

            // System.out.printf("InvConUserBookkeeping2 name: %s, value: %f, mod: %b\n", this.getVarInfo().name(), val, mod);

            return new ValueAndModified(val_string, mod);

        } else if (key_var2_index!=-1){

            long sub_key_size = val3_array[key_var2_index];
            long sub_key_start_index = 0;
            for (int i=0; i<key_var2_index; i++){
                sub_key_start_index +=  val3_array[i];
            }
            // find sub key index in the array sub_keys_var
            // int index = ArraysPlume.indexOf(val2_array, key_var2, sub_key_start_index, sub_key_start_index+sub_key_size);
            int index = -1;
            for (long i= sub_key_start_index; i< sub_key_start_index+sub_key_size;i++){
                if (val2_array[(int)i].equals(key_var1)){
                    index = (int)i;
                    break;
                }
            }
            System.out.printf("InvConUserBookkeeping2 name: %s, index: %d in [%d, %d)\n", this.getVarInfo().name(), index, sub_key_start_index, sub_key_start_index+sub_key_size);
            if (index==-1){
                // double val = 0;
                // return new ValueAndModified(val, ValueTuple.UNMODIFIED);
                // return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
                return ValueAndModified.MISSING_NONSENSICAL;
            }
            // get values_var[index]
            java.math.BigInteger val = val4_array[index];
            String val_string = Intern.intern(val.toString());
            
            System.out.printf("InvConUserBookkeeping2 name: %s, value: %f, mod: %b\n", this.getVarInfo().name(), val, mod);

            return new ValueAndModified(val_string, mod);
            // return ValueAndModified.MISSING_NONSENSICAL;
        }else {
            // return new ValueAndModified(0.0, ValueTuple.UNMODIFIED);
            return ValueAndModified.MISSING_NONSENSICAL;
        }
    }

    @Override
    protected VarInfo makeVarInfo() {
        // TODO Auto-generated method stub
        // return VarInfo.make_function("bookkeeping", VarInfo.make_subscript(values_var(), key_var1(), 0), key_var2());
        return VarInfo.make_subscript(values_var(),  VarInfo.make_function("pair", key_var1(), key_var2()), 0);
        // return VarInfo.make_subscript(values_var(),  key_var1(), 0);
    }

    @Override
    public boolean isSameFormula(Derivation other) {
        // TODO Auto-generated method stub
        // return false;
        return (other instanceof InvConUserBookkeeping2);
    }

    /** Returns the csharp name. */
    @SideEffectFree
    @Override
    public String csharp_name(String index) {
        String key_name1 = key_var1().csharp_name();
        String key_name2 = key_var2().csharp_name();
        // We do not need to check if seqvar().isPrestate() because it is redundant.
        return values_var().csharp_name() + ".ValueOf(" + key_name1 + ", "+ key_name2 + ")";
    }

    /** Returns the ESC name. */
    @SideEffectFree
    @Override
    public String esc_name(String index) {
        return String.format(
        "%s[%s][%s]",
        values_var().esc_name(), key_var1().esc_name(), key_var2().esc_name());
    }
}
