package daikon.derive.unary;

import daikon.Daikon;
import daikon.ProglangType;
import daikon.VarInfo;
import daikon.inv.OutputFormat;
import java.util.ArrayList;
import org.checkerframework.checker.nullness.qual.Nullable;

public final class SequenceMinMaxSumFactory extends UnaryDerivationFactory {

  @Override
  public UnaryDerivation @Nullable [] instantiate(VarInfo vi) {
    // System.out.println("SequenceMinMaxSumFactory.instantiate(" +  vi.rep_type + ")");
    // if (vi.rep_type != ProglangType.INT_ARRAY ) {
      //   return null;
      // }
      
      // update by liuye 
    if (vi.rep_type != ProglangType.INT_ARRAY && vi.rep_type != ProglangType.DOUBLE_ARRAY  && vi.rep_type != ProglangType.LONG_PRIMITIVE_ARRAY && vi.rep_type != ProglangType.BIGINT_ARRAY) {
        return null;
    }
    // System.out.println("SequenceMinMaxSumFactory.instantiate(" + vi.type + " " +  vi.rep_type + ")");
    // System.out.println("SequenceSum.dkconfig_enabled: "+ SequenceSum.dkconfig_enabled);
    // System.out.println("vi.type.isArray(): "+ vi.type.isArray());
    // System.out.println("vi.type.elementIsIntegral(): "+ vi.type.elementIsIntegral());
    // System.out.println("vi.type.elementIsFloat(): "+ vi.type.elementIsFloat());
    // System.out.println("vi.type.base(): "+ vi.type.base());
    // System.out.println("Daikon.output_format: "+ Daikon.output_format+ ";" + (Daikon.output_format==OutputFormat.DAIKON));
    if (!vi.type.isArray()) {
      return null;
    }
    if (!vi.type.elementIsIntegral() && !vi.type.elementIsFloat() && !vi.type.elementIsBigInt()) {
      return null;
    }
    if (vi.type.base() == "char") // interned
    return null;
    // Should be reversed at some point; for now, will improve run time.
    if (Daikon.output_format != OutputFormat.DAIKON) {
      return null;
    }
   
    ArrayList<UnaryDerivation> result = new ArrayList<>(3);
    if (SequenceMin.dkconfig_enabled) {
      result.add(new SequenceMin(vi));
    }
    if (SequenceMax.dkconfig_enabled) {
      result.add(new SequenceMax(vi));
    }
    if (SequenceSum.dkconfig_enabled) {
      result.add(new SequenceSum(vi));
      // System.out.println("SequenceSum was enabled");
    }

    if (result.size() == 0) {
      return null;
    }

    return result.toArray(new UnaryDerivation[result.size()]);
  }
}
